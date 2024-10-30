# backend/services/atendimento_service.py

import logging
from datetime import datetime, timedelta
from faker import Faker
import random
from ...models import Paciente, Clinica, Doenca, Medico, Atendimento, Prontuario, Bairro, ProfissionalSaude
from .agendamento_service import gerar_agendamento
from ...utils.mortalidade_utils import aplicar_taxa_mortalidade_bairros
from ...utils.escolha_utils import escolher_clinica, selecionar_medico, gerar_status_conclusao, validar_ano_atendimento

fake = Faker('pt_BR')

def generate_atendimentos(session, qtd_atendimentos):
    logging.info(f"Iniciando a geração de {qtd_atendimentos} atendimentos.")
    
    # Carregar dados e verificar individualmente
    profissionais = session.query(ProfissionalSaude).all()
    pacientes = session.query(Paciente).all()
    doencas = session.query(Doenca).all()
    clinicas_publicas = session.query(Clinica).filter(Clinica.tipo == 'Pública').all()
    clinicas_privadas = session.query(Clinica).filter(Clinica.tipo == 'Privada').all()
    medicos = session.query(Medico).all()
    bairros = session.query(Bairro).all()

    # Validar dados e log detalhado
    if not profissionais:
        logging.error("Dados insuficientes: faltam profissionais de saúde.")
    if not pacientes:
        logging.error("Dados insuficientes: faltam pacientes.")
    if not doencas:
        logging.error("Dados insuficientes: faltam doenças.")
    if not clinicas_publicas or not clinicas_privadas:
        logging.error("Dados insuficientes: faltam clínicas públicas ou privadas.")
    if not medicos:
        logging.error("Dados insuficientes: faltam médicos.")
    if not bairros:
        logging.error("Dados insuficientes: faltam bairros.")
    if not (profissionais and pacientes and doencas and clinicas_publicas and clinicas_privadas and medicos and bairros):
        logging.error("Abortando geração de atendimentos devido a dados insuficientes.")
        return

    taxa_mortalidade_bairros = aplicar_taxa_mortalidade_bairros(bairros)

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
            reagendar_atendimento(session, paciente, clinica, doenca, "Capacidade excedida")
            continue

        medico = selecionar_medico(paciente, doenca, medicos)
        if not medico:
            logging.warning(f"Falta de médico para o paciente {paciente.nome}, reagendando.")
            reagendar_atendimento(session, paciente, clinica, doenca, "Falta de médico")
            continue

        hora_atendimento = fake.time_object()
        hora_conclusao = (datetime.combine(datetime.today(), hora_atendimento) + timedelta(minutes=random.randint(15, 120))).time()
        status = validar_ano_atendimento(data_atendimento)

        atendimento = Atendimento(
            id_paciente=paciente.id,
            id_bairro=bairro.id,
            id_doenca=doenca.id,
            id_clinica=clinica.id,
            id_medico=medico.id,
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

        if atendimentos_gerados % 5000 == 0:
            session.bulk_save_objects(prontuarios_batch)
            session.commit()
            prontuarios_batch.clear()

    session.bulk_save_objects(prontuarios_batch)
    session.commit()
    logging.info(f"{atendimentos_gerados} atendimentos foram gerados com sucesso.")

def reagendar_atendimento(session, paciente, clinica, doenca, motivo):
    try:
        gerar_agendamento(session, paciente, clinica, doenca, motivo)
    except Exception as e:
        logging.error(f"Erro ao reagendar atendimento para paciente {paciente.nome}: {e}")
