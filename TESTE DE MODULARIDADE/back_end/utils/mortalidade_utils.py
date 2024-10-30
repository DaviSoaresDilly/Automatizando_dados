# backend/utils/mortalidade_utils.py

import random
import logging

def aplicar_taxa_mortalidade_bairros(bairros):
    """
    Aplica uma taxa de mortalidade para cada bairro, retornando um dicionário com as taxas de mortalidade.
    A taxa pode variar de acordo com as condições do bairro (simulação).

    :param bairros: Lista de instâncias de Bairro.
    :return: Dicionário com o ID do bairro como chave e a taxa de mortalidade como valor.
    """
    taxa_mortalidade_bairros = {}

    for bairro in bairros:
        # Define a taxa de mortalidade com base em critérios específicos do bairro
        taxa_mortalidade = random.uniform(0.01, 0.05)  # Exemplo: taxa entre 1% e 5%
        taxa_mortalidade_bairros[bairro.id] = taxa_mortalidade
        logging.debug(f"Bairro {bairro.nome}: taxa de mortalidade definida em {taxa_mortalidade:.2%}")

    logging.info("Taxas de mortalidade aplicadas a todos os bairros.")
    return taxa_mortalidade_bairros

def verificar_obito(probabilidade_mortalidade):
    """
    Verifica se um óbito ocorre com base em uma probabilidade de mortalidade.

    :param probabilidade_mortalidade: Probabilidade de óbito (valor entre 0 e 1).
    :return: Booleano indicando se o óbito ocorreu.
    """
    obito_ocorreu = random.random() < probabilidade_mortalidade
    logging.debug(f"Óbito {'ocorreu' if obito_ocorreu else 'não ocorreu'} com probabilidade de {probabilidade_mortalidade:.2%}")
    return obito_ocorreu
