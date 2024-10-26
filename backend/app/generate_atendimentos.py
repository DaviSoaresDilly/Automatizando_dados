# app/generate_atendimentos.py
import logging
from .models import Agendamento, Atendimento, AtendimentoPulado, Prontuario, Paciente, Bairro, Doenca, Clinica, Medico, AtendimentoProfissional, ProfissionalSaude
from datetime import datetime, timedelta
from faker import Faker
import random

fake = Faker('pt_BR')

# Configuração de logging detalhado
logging.basicConfig(level=logging.INFO)

# Função para calcular a taxa de mortalidade ajustada para o bairro
def calcular_taxa_mortalidade(populacao_bairro, taxa_mortalidade_bh, populacao_bh):
    if populacao_bairro > 0:
        proporcao_populacional = populacao_bairro / populacao_bh
        return taxa_mortalidade_bh * proporcao_populacional
    return 0.0

# Taxa de mortalidade em BH e população total
taxa_mortalidade_bh = 0.00753  # Média de 0.753% de mortalidade
populacao_bh = 2_416_339  # População de Belo Horizonte

# Função para aplicar a taxa de mortalidade ajustada para cada bairro
def aplicar_taxa_mortalidade_bairros(bairros):
    taxa_mortalidade_bairros = {}
    for bairro in bairros:
        taxa_mortalidade = calcular_taxa_mortalidade(bairro.pop_total, taxa_mortalidade_bh, populacao_bh)
        logging.debug(f"Taxa de mortalidade ajustada para o bairro {bairro.nome}: {taxa_mortalidade:.6f}")
        taxa_mortalidade_bairros[bairro.id] = taxa_mortalidade
    return taxa_mortalidade_bairros

# Função para gerar um agendamento para o paciente
def gerar_agendamento(session, paciente, clinica, doenca, motivo):
    """Cria um agendamento para o paciente, evitando duplicados."""
    if not session.query(Agendamento).filter_by(id_paciente=paciente.id, id_doenca=doenca.id, id_clinica=clinica.id).first():
        data_agendada = datetime.now() + timedelta(days=random.randint(1, 30))
        agendamento = Agendamento(
            id_paciente=paciente.id,
            id_clinica=clinica.id if clinica else None,
            id_doenca=doenca.id,
            data_agendada=data_agendada,
            motivo=motivo,
        )
        session.add(agendamento)

# Função principal para geração de atendimentos
def generate_atendimentos(session, qtd_atendimentos):
    logging.info(f"Iniciando a geração de {qtd_atendimentos} atendimentos.")

    # Carregar dados e verificar
    profissionais = session.query(ProfissionalSaude).all()
    pacientes = session.query(Paciente).all()
    doencas = session.query(Doenca).all()
    clinicas_publicas = session.query(Clinica).filter(Clinica.tipo == 'Pública').all()
    clinicas_privadas = session.query(Clinica).filter(Clinica.tipo == 'Privada').all()
    medicos = session.query(Medico).all()
    bairros = session.query(Bairro).all()

    if not (profissionais and pacientes and doencas and clinicas_publicas and clinicas_privadas and medicos and bairros):
        logging.error("Dados insuficientes: faltam profissionais, pacientes, doenças, clínicas ou médicos.")
        return

    # Aplicar a taxa de mortalidade ajustada para cada bairro
    taxa_mortalidade_bairros = aplicar_taxa_mortalidade_bairros(bairros)

    # Configuração para geração de atendimentos
    data_inicio = datetime(2022, 1, 1)
    dias_entre = (datetime(2024, 12, 31) - data_inicio).days
    atendimentos_gerados = 0
    prontuarios_batch = []

    while atendimentos_gerados < qtd_atendimentos:
        data_atendimento = data_inicio + timedelta(days=random.randint(0, dias_entre))
        paciente = random.choice(pacientes)
        bairro = random.choice(bairros)
        doenca = random.choice(doencas)
        clinica = escolher_clinica(doenca, clinicas_publicas, clinicas_privadas)
        if not clinica:
            logging.warning(f"Capacidade excedida para o paciente {paciente.nome}, reagendando.")
            gerar_agendamento(session, paciente, clinica, doenca, "Capacidade excedida")
            continue

        medico = selecionar_medico(paciente, doenca, medicos)
        if not medico:
            logging.warning(f"Falta de médico para o paciente {paciente.nome}, reagendando.")
            gerar_agendamento(session, paciente, clinica, doenca, "Falta de médico")
            continue

        hora_atendimento = fake.time_object()
        hora_conclusao = (datetime.combine(datetime.today(), hora_atendimento) + timedelta(minutes=random.randint(15, 120))).time()
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
        session.add(atendimento)
        session.flush()

        prontuario = Prontuario(
            id_paciente=paciente.id,
            id_atendimento=atendimento.id,
            id_medico=medico.id,
            descricao=fake.text(),
            data=data_atendimento.date(),
            hora=hora_atendimento,
            status_conclusao=gerar_status_conclusao(doenca, clinica, bairro, taxa_mortalidade_bairros[bairro.id])
        )
        prontuarios_batch.append(prontuario)

        atendimentos_gerados += 1

        if atendimentos_gerados % 1000 == 0:
            session.bulk_save_objects(prontuarios_batch)
            session.commit()
            prontuarios_batch.clear()

    session.bulk_save_objects(prontuarios_batch)
    session.commit()

    logging.info(f"{atendimentos_gerados} atendimentos foram gerados com sucesso.")

# Funções auxiliares para a geração de atendimentos
def escolher_clinica(doenca, clinicas_publicas, clinicas_privadas):
    """Escolhe a clínica adequada para o atendimento baseado na gravidade da doença."""
    if doenca.gravidade in ['Muito Grave', 'Grave']:
        return next((c for c in clinicas_publicas if 'UPA' in c.nome), None) or random.choice(clinicas_publicas)
    elif doenca.gravidade == 'Moderada':
        return next((c for c in clinicas_publicas if 'Centro de Saúde' in c.nome), None) or random.choice(clinicas_privadas)
    return random.choice(clinicas_privadas)

def selecionar_medico(paciente, doenca, medicos):
    """Seleciona um médico disponível com base na especialidade necessária."""
    if doenca.requer_cirurgia:
        return next((m for m in medicos if m.especialidade == doenca.especialista), None) or random.choice(medicos)
    if paciente.idade <= 12:
        return next((m for m in medicos if m.especialidade == 'Pediatria'), None) or random.choice(medicos)
    return next((m for m in medicos if m.especialidade == 'Clínico Geral'), None) or random.choice(medicos)

def gerar_status_conclusao(doenca, clinica, bairro, taxa_mortalidade):
    """Define o status de conclusão do prontuário considerando fatores de risco e mortalidade."""
    if doenca.requer_cirurgia and 'UPA' in clinica.nome:
        return 'Encaminhado para hospital'

    if random.random() < taxa_mortalidade:
        return 'Óbito'
    
    return random.choice(['Curado', 'Em tratamento', 'Sem retorno'])

def validar_ano_atendimento(data_atendimento):
    """Define o status do atendimento com base no ano de realização."""
    ano = data_atendimento.year
    if ano in [2022, 2023]:
        return 'Concluído'
    elif ano == 2024:
        return random.choice(['Concluído', 'Em andamento', 'Cancelado', 'Aguardando'])
    return 'Concluído'
