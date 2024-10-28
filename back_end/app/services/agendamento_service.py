# backend/services/agendamento_service.py

from datetime import datetime, timedelta
from faker import Faker
import random
import logging
from ...models import Agendamento

fake = Faker('pt_BR')

def gerar_agendamento(session, paciente, clinica, doenca, motivo):
    """
    Cria um agendamento para um paciente em uma clínica específica, incluindo o motivo do reagendamento.
    
    :param session: Sessão do banco de dados
    :param paciente: Instância do paciente que necessita do agendamento
    :param clinica: Instância da clínica onde o paciente será atendido
    :param doenca: Instância da doença para a qual o paciente precisa de atendimento
    :param motivo: Motivo pelo qual o atendimento foi reagendado (ex: "Capacidade excedida" ou "Falta de médico")
    """
    data_agendamento = datetime.now().date() + timedelta(days=random.randint(1, 15))
    
    agendamento = Agendamento(
        id_paciente=paciente.id,
        id_clinica=clinica.id,
        id_doenca=doenca.id,
        data_agendamento=data_agendamento,
        motivo=motivo
    )
    
    try:
        session.add(agendamento)
        session.commit()
        logging.info(f"Agendamento criado para o paciente {paciente.nome} na clínica {clinica.nome} para o dia {data_agendamento} devido a: {motivo}")
    except Exception as e:
        session.rollback()
        logging.error(f"Erro ao criar agendamento para paciente {paciente.nome}: {e}")

def atualizar_status_agendamento(session, agendamento_id, novo_status):
    """
    Atualiza o status de um agendamento existente.

    :param session: Sessão do banco de dados
    :param agendamento_id: ID do agendamento a ser atualizado
    :param novo_status: Novo status para o agendamento (ex: "Concluído", "Cancelado")
    """
    agendamento = session.query(Agendamento).filter_by(id=agendamento_id).first()
    if agendamento:
        try:
            agendamento.status = novo_status
            session.commit()
            logging.info(f"Status do agendamento ID {agendamento_id} atualizado para: {novo_status}")
        except Exception as e:
            session.rollback()
            logging.error(f"Falha ao atualizar status do agendamento ID {agendamento_id}: {e}")
    else:
        logging.warning(f"Agendamento com ID {agendamento_id} não encontrado.")

def obter_agendamentos_pendentes(session, data_limite=None):
    """
    Retorna uma lista de agendamentos pendentes até uma data específica (opcional).

    :param session: Sessão do banco de dados
    :param data_limite: Data limite opcional para filtrar agendamentos
    :return: Lista de agendamentos pendentes
    """
    query = session.query(Agendamento.id, Agendamento.data_agendamento).filter(Agendamento.status == 'Pendente')
    if data_limite:
        query = query.filter(Agendamento.data_agendamento <= data_limite)
    agendamentos = query.all()
    logging.info(f"{len(agendamentos)} agendamentos pendentes encontrados até a data {data_limite or 'atual'}.")
    return agendamentos
