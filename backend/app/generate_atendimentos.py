import logging
from .models import Atendimento, AtendimentoPulado, Prontuario, Paciente, Bairro, Doenca, Clinica, Medico, AtendimentoProfissional, ProfissionalSaude
from faker import Faker
from datetime import datetime, timedelta
import random
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

fake = Faker('pt_BR')

# Helper functions
def str_to_time(time_str):
    """Converte uma string de hora ('HH:MM:SS') para um objeto time."""
    return datetime.strptime(time_str, '%H:%M:%S').time()

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
        session.rollback()  # Evita duplicações

# Função principal
def generate_atendimentos(session, qtd_atendimentos):
    """Gera e insere atendimentos fictícios de 2022 a 2024 com grupos de risco priorizados."""
    logging.info(f"Iniciando a geração de {qtd_atendimentos} atendimentos.")
    atendimentos = []
    atendimentos_pulados = []

    # Carregar todos os dados necessários em uma única operação
    pacientes = session.query(Paciente).all()
    bairros = session.query(Bairro).all()
    doencas = session.query(Doenca).all()
    clinicas_publicas = session.query(Clinica).filter_by(tipo='Pública').all()
    clinicas_privadas = session.query(Clinica).filter_by(tipo='Privada').all()
    medicos = session.query(Medico).all()
    profissionais = session.query(ProfissionalSaude).all()

    if not pacientes or not bairros or not doencas or not clinicas_publicas or not clinicas_privadas or not medicos or not profissionais:
        logging.error("Dados insuficientes para gerar atendimentos.")
        return

    # Definindo o período de atendimento
    data_inicio = datetime(2022, 1, 1)
    dias_entre = (datetime(2024, 12, 31) - data_inicio).days

    for i in range(qtd_atendimentos):
        try:
            # Gerar uma data de atendimento aleatória dentro do período de 3 anos
            data_atendimento = data_inicio + timedelta(days=random.randint(0, dias_entre))
            logging.info(f"Data de atendimento gerada: {data_atendimento}")

            # Selecionar um paciente, bairro e doença aleatoriamente
            paciente = random.choice(pacientes)
            logging.info(f"Paciente selecionado: {paciente.id}")

            bairro, doenca = random.choice(bairros), random.choice(doencas)
            logging.info(f"Bairro selecionado: {bairro.id}, Doença selecionada: {doenca.id}")

            # Selecionar uma clínica adequada
            clinica = escolher_clinica(doenca, clinicas_publicas, clinicas_privadas)
            if not clinica:
                motivo = "Capacidade excedida"
                registrar_atendimento_pulado(session, paciente, bairro, doenca, motivo, data_atendimento.date())
                logging.info(f"Atendimento {i+1}/{qtd_atendimentos} pulado: {motivo}")
                continue

            # Selecionar um médico adequado
            medico = selecionar_medico(paciente, doenca, medicos)
            if not medico:
                motivo = "Falta de médico"
                registrar_atendimento_pulado(session, paciente, bairro, doenca, motivo, data_atendimento.date())
                logging.info(f"Atendimento {i+1}/{qtd_atendimentos} pulado: {motivo}")
                continue

            # Gerar hora de atendimento e conclusão
            hora_atendimento = str_to_time(fake.time())
            hora_conclusao = str_to_time(fake.time())
            if hora_conclusao <= hora_atendimento:
                hora_conclusao = (datetime.combine(datetime.today(), hora_atendimento) + timedelta(minutes=random.randint(15, 60))).time()

            # Definir o status do atendimento com base no ano
            status = validar_ano_atendimento(data_atendimento)

            # Criar o atendimento
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
                id_atendimento=atendimento.id,
                id_medico=medico.id,
                descricao=fake.text(),
                data=data_atendimento.date(),
                hora=hora_atendimento,
                status_conclusao=verificar_encaminhamento(doenca, clinica)
            )
            session.add(prontuario)

            # Adicionar médico ao atendimento
            verificar_e_adicionar_atendimento_profissional(session, atendimento, medico, 'Consulta Médica')

            # Adicionar enfermeiro/técnico ao atendimento
            enfermeiro_ou_tecnico = selecionar_enfermeiro_ou_tecnico(profissionais)
            if enfermeiro_ou_tecnico:
                verificar_e_adicionar_atendimento_profissional(session, atendimento, enfermeiro_ou_tecnico, 'Acompanhamento de Enfermagem')

            logging.info(f"Atendimento {i+1}/{qtd_atendimentos} gerado com sucesso.")
        except SQLAlchemyError as e:
            logging.error(f"Erro ao gerar atendimento {i+1}/{qtd_atendimentos}: {e}")
            session.rollback()

    # Commit de todos os atendimentos, prontuários e atendimentos pulados
    try:
        session.commit()
        logging.info(f"{len(atendimentos)} atendimentos gerados e inseridos com sucesso.")
        logging.info(f"{len(atendimentos_pulados)} atendimentos pulados.")
    except SQLAlchemyError as e:
        logging.error(f"Erro ao confirmar os atendimentos: {e}")
        session.rollback()

def registrar_atendimento_pulado(session, paciente, bairro, doenca, motivo, data_tentativa):
    """Registra um atendimento que foi pulado."""
    try:
        atendimento_pulado = AtendimentoPulado(
            id_paciente=paciente.id,
            id_bairro=bairro.id,
            id_doenca=doenca.id,
            motivo=motivo,
            data_tentativa=data_tentativa
        )
        session.add(atendimento_pulado)
        session.flush()
        logging.info(f"Atendimento pulado registrado: {motivo}")
    except SQLAlchemyError as e:
        logging.error(f"Erro ao registrar atendimento pulado: {e}")
        session.rollback()

def escolher_clinica(doenca, clinicas_publicas, clinicas_privadas):
    """Escolhe a clínica adequada com base na gravidade da doença."""
    if doenca.gravidade in ['Muito Grave', 'Grave']:
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

def verificar_encaminhamento(doenca, clinica):
    """Verifica a necessidade de encaminhamento de emergência."""
    if doenca.requer_cirurgia and 'UPA' in clinica.nome:
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