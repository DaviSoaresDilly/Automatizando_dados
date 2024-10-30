# backend/utils/escolha_utils.py

import random
import logging
from datetime import datetime

from back_end.utils.mortalidade_utils import verificar_obito

def escolher_clinica(doenca, clinicas_publicas, clinicas_privadas):
    """
    Seleciona a clínica apropriada com base na gravidade da doença.
    
    :param doenca: Instância de Doenca.
    :param clinicas_publicas: Lista de clínicas públicas.
    :param clinicas_privadas: Lista de clínicas privadas.
    :return: Instância da clínica selecionada ou None se não houver capacidade.
    """
    clinica = random.choice(clinicas_privadas) if doenca.gravidade > 7 else random.choice(clinicas_publicas)
    
    # Simulação da capacidade da clínica (ajustar conforme necessidade)
    capacidade_excedida = random.choice([True, False])
    if capacidade_excedida:
        logging.debug(f"Capacidade excedida na clínica {clinica.nome}.")
        return None
    else:
        logging.debug(f"Clínica selecionada: {clinica.nome} para a doença {doenca.nome}.")
        return clinica

def selecionar_medico(paciente, doenca, medicos):
    """
    Seleciona um médico com base na especialidade da doença.
    
    :param paciente: Instância do paciente.
    :param doenca: Instância de Doenca.
    :param medicos: Lista de instâncias de Medico.
    :return: Instância do médico selecionado ou None se não houver médicos disponíveis.
    """
    medicos_especialistas = [medico for medico in medicos if medico.especialidade == doenca.especialidade]
    if not medicos_especialistas:
        logging.warning(f"Sem médicos disponíveis para a especialidade {doenca.especialidade}.")
        return None

    medico = random.choice(medicos_especialistas)
    logging.debug(f"Médico {medico.nome} selecionado para o paciente {paciente.nome} com a doença {doenca.nome}.")
    return medico

def gerar_status_conclusao(doenca, clinica, bairro, taxa_mortalidade):
    """
    Gera o status de conclusão com base na taxa de mortalidade e na gravidade da doença.
    
    :param doenca: Instância de Doenca.
    :param clinica: Instância de Clinica.
    :param bairro: Instância de Bairro.
    :param taxa_mortalidade: Taxa de mortalidade específica do bairro.
    :return: Status de conclusão (Ex: "Concluído", "Óbito").
    """
    if doenca.gravidade > 7 and verificar_obito(taxa_mortalidade):
        logging.debug(f"Óbito ocorrido para paciente no bairro {bairro.nome} com gravidade {doenca.gravidade}.")
        return "Óbito"
    return "Concluído"

def validar_ano_atendimento(data_atendimento):
    """
    Valida o ano do atendimento para verificar se é um dado histórico (pré-2023).
    
    :param data_atendimento: Data do atendimento.
    :return: "Concluído" para dados atuais, "Histórico" para dados anteriores a 2023.
    """
    ano_limite = 2023
    status = "Histórico" if data_atendimento.year < ano_limite else "Concluído"
    logging.debug(f"Data de atendimento {data_atendimento}: Status definido como {status}.")
    return status
