import logging
from .models import Atendimento, Prontuario, Paciente, Bairro, Doenca, Clinica, Medico, AtendimentoProfissional, ProfissionalSaude
from faker import Faker
from datetime import datetime, timedelta
import random
from sqlalchemy.exc import IntegrityError

fake = Faker('pt_BR')

# Helper functions
def str_to_time(time_str):
    """Converte uma string de hora ('HH:MM:SS') para um objeto time."""
    return datetime.strptime(time_str, '%H:%M:%S').time()

def is_grupo_de_risco(paciente):
    """Verifica se o paciente pertence a um grupo de risco (idosos >= 60, gestantes)."""
    return paciente.idade >= 60 or 'Gestante' in paciente.sexo

def calcular_frequencia_grupo_risco(paciente):
    """Ajusta a frequência de atendimentos para grupos de risco."""
    return random.random() < 0.45 if is_grupo_de_risco(paciente) else True

def selecionar_enfermeiro_ou_tecnico(profissionais):
    """Seleciona enfermeiro ou técnico de enfermagem para o atendimento."""
    enfermeiros_tecnicos = [p for p in profissionais if p.tipo in ['Enfermeiro', 'Técnico de Enfermagem']]
    return random.choice(enfermeiros_tecnicos) if enfermeiros_tecnicos else None

def verificar_e_adicionar_atendimento_profissional(session, atendimento, profissional, funcao):
    """Verifica duplicidade e adiciona o profissional ao atendimento se não houver duplicata."""
    try:
        atendimento_profissional = AtendimentoProfissional(
            id_atendimento=atendimento.id,
            id_profissional=profissional.id,
            funcao=funcao
        )
        session.add(atendimento_profissional)
        session.flush()  # Verifica a integridade
    except IntegrityError:
        session.rollback()  # Evita a duplicação por causa da constraint UNIQUE

# Função principal
def generate_atendimentos(session, qtd_atendimentos):
    """Gera e insere atendimentos fictícios de 2022 a 2024 com grupos de risco priorizados."""
    
    # Pré-carregar todos os dados necessários em uma única consulta
    profissionais = session.query(ProfissionalSaude).all()
    pacientes = session.query(Paciente).all()
    doencas = session.query(Doenca).all()
    bairros = session.query(Bairro).all()
    clinicas_publicas = session.query(Clinica).filter(Clinica.tipo == 'Pública').all()
    clinicas_privadas = session.query(Clinica).filter(Clinica.tipo == 'Privada').all()
    medicos = session.query(Medico).all()

    if not (profissionais and pacientes and doencas and bairros and clinicas_publicas and clinicas_privadas and medicos):
        logging.error("Dados insuficientes: Faltam profissionais, pacientes, doenças, bairros, clínicas ou médicos.")
        return

    # Definindo o período de atendimento
    data_inicio = datetime(2022, 1, 1)
    dias_entre = (datetime(2024, 12, 31) - data_inicio).days

    atendimentos = []
    
    for _ in range(qtd_atendimentos):
        data_atendimento = data_inicio + timedelta(days=random.randint(0, dias_entre))

        paciente = random.choice(pacientes)
        if not calcular_frequencia_grupo_risco(paciente):
            continue

        bairro, doenca = random.choice(bairros), random.choice(doencas)
        grupo_risco = is_grupo_de_risco(paciente)
        clinica = escolher_clinica(doenca, grupo_risco, clinicas_publicas, clinicas_privadas)
        if not clinica:
            continue

        medico = selecionar_medico(paciente, doenca, medicos)
        if not medico:
            continue

        # Hora de atendimento e conclusão
        hora_atendimento = str_to_time(fake.time())
        hora_conclusao = str_to_time(fake.time())
        if hora_conclusao <= hora_atendimento:
            hora_conclusao = (datetime.combine(datetime.today(), hora_atendimento) + timedelta(minutes=random.randint(15, 60))).time()

        # Cria atendimento
        status = validar_ano_atendimento(data_atendimento)
        atendimento = Atendimento(
            id_paciente=paciente.id,
            id_bairro=bairro.id,
            id_doenca=doenca.id,
            id_clinica=clinica.id,
            data_atendimento=data_atendimento.date(),
            status=status,
            hora_atendimento=hora_atendimento,
            hora_conclusao=hora_conclusao
        )
        atendimentos.append(atendimento)
        session.add(atendimento)
        session.flush()

        # Criar prontuário vinculado ao atendimento gerado
        prontuario = Prontuario(
            id_paciente=paciente.id,
            id_atendimento=atendimento.id,  # Vincular corretamente ao atendimento
            id_medico=medico.id,
            descricao=fake.text(),
            data=data_atendimento.date(),
            hora=hora_atendimento,
            status_conclusao=verificar_encaminhamento(doenca, clinica, grupo_risco)
        )
        session.add(prontuario)

        # Adicionar médico ao atendimento
        verificar_e_adicionar_atendimento_profissional(session, atendimento, medico, 'Consulta Médica')

        # Adicionar enfermeiro/técnico ao atendimento
        enfermeiro_ou_tecnico = selecionar_enfermeiro_ou_tecnico(profissionais)
        if enfermeiro_ou_tecnico:
            verificar_e_adicionar_atendimento_profissional(session, atendimento, enfermeiro_ou_tecnico, 'Acompanhamento de Enfermagem')

    # Commit de todos os atendimentos e prontuários
    session.commit()

def escolher_clinica(doenca, grupo_risco, clinicas_publicas, clinicas_privadas):
    """Escolhe a clínica adequada com base na gravidade e grupo de risco."""
    if doenca.gravidade in ['Muito Grave', 'Grave'] or grupo_risco:
        return next((c for c in clinicas_publicas if 'UPA' in c.nome), None) or random.choice(clinicas_publicas)
    elif doenca.gravidade == 'Moderada':
        return next((c for c in clinicas_publicas if 'Centro de Saúde' in c.nome), None) or random.choice(clinicas_privadas)
    return random.choice(clinicas_privadas)

def selecionar_medico(paciente, doenca, medicos):
    """Seleciona o médico responsável pelo atendimento."""
    if paciente.idade <= 12:
        return next((m for m in medicos if m.especialidade == 'Pediatria'), None) or random.choice(medicos)
    if doenca.requer_cirurgia:
        return next((m for m in medicos if m.especialidade == doenca.especialista), None) or random.choice(medicos)
    return next((m for m in medicos if m.especialidade == 'Clínico Geral'), None) or random.choice(medicos)

def verificar_encaminhamento(doenca, clinica, grupo_risco):
    """Verifica a necessidade de encaminhamento de emergência."""
    if doenca.requer_cirurgia and 'UPA' in clinica.nome:
        return 'Encaminhado para hospital'
    if grupo_risco and doenca.gravidade in ['Grave', 'Muito Grave']:
        return 'Encaminhado para hospital'
    return 'Concluído'

def validar_ano_atendimento(data_atendimento):
    """Valida o status do atendimento com base no ano."""
    ano = data_atendimento.year
    if ano in [2022, 2023]:
        return 'Concluído'
    elif ano == 2024:
        return random.choice(['Concluído', 'Em andamento', 'Cancelado', 'Aguardando'])
    return 'Concluído'
