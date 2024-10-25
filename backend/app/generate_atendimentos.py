# app/generate_atendimentos.py
import logging
from .models import Agendamento, Atendimento, AtendimentoPulado, Prontuario, Paciente, Bairro, Doenca, Clinica, Medico, AtendimentoProfissional, ProfissionalSaude
from datetime import datetime, timedelta
from faker import Faker
import random

fake = Faker('pt_BR')

# Configuração de logging
logging.basicConfig(level=logging.INFO)

def calcular_taxa_mortalidade(populacao_bairro, taxa_mortalidade_bh, populacao_bh):
    """
    Calcula a taxa de mortalidade ajustada para o bairro com base na taxa de mortalidade de Belo Horizonte.
    """
    proporcao_populacional = populacao_bairro / populacao_bh
    return taxa_mortalidade_bh * proporcao_populacional

# Taxa de mortalidade em BH (baseada nos anos de 2022 e 2023) e população total
taxa_mortalidade_bh = 0.00753  # Média de 0.753% de mortalidade
populacao_bh = 2_416_339  # População de Belo Horizonte

# Aplicando a taxa para cada bairro
def aplicar_taxa_mortalidade_bairros(bairros):
    taxa_mortalidade_bairros = {}
    for bairro in bairros:
        taxa_mortalidade = calcular_taxa_mortalidade(bairro.pop_total, taxa_mortalidade_bh, populacao_bh)
        logging.info(f"Taxa de mortalidade ajustada para o bairro {bairro.nome}: {taxa_mortalidade:.6f}")
        taxa_mortalidade_bairros[bairro.id] = taxa_mortalidade
    return taxa_mortalidade_bairros
    
# Função para gerar agendamento
def gerar_agendamento(session, paciente, clinica, doenca, motivo):
    """Cria um agendamento para o paciente."""
    data_agendada = datetime.now() + timedelta(days=random.randint(1, 30))  # Agendar para até 30 dias no futuro
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

    # Carregar dados
    profissionais = session.query(ProfissionalSaude).all()
    pacientes = session.query(Paciente).all()
    doencas = session.query(Doenca).all()
    clinicas_publicas = session.query(Clinica).filter(Clinica.tipo == 'Pública').all()
    clinicas_privadas = session.query(Clinica).filter(Clinica.tipo == 'Privada').all()
    medicos = session.query(Medico).all()
    bairros = session.query(Bairro).all()

    # Validar se todos os dados necessários estão disponíveis
    if not (profissionais and pacientes and doencas and clinicas_publicas and clinicas_privadas and medicos and bairros):
        logging.error("Dados insuficientes: faltam profissionais, pacientes, doenças, clínicas ou médicos.")
        return

    # Aplicar a taxa de mortalidade ajustada para cada bairro
    taxa_mortalidade_bairros = aplicar_taxa_mortalidade_bairros(bairros)

    # Definir início de atendimento e capacidade diária
    data_inicio = datetime(2022, 1, 1)
    dias_entre = (datetime(2024, 12, 31) - data_inicio).days

    atendimentos_gerados = 0
    atendimentos_batch = []
    prontuarios_batch = []

    while atendimentos_gerados < qtd_atendimentos:
        # Gera a data do atendimento e verifica a capacidade do dia
        data_atendimento = data_inicio + timedelta(days=random.randint(0, dias_entre))

        # Seleciona paciente, bairro e doença
        paciente = random.choice(pacientes)
        bairro = random.choice(bairros)
        doenca = random.choice(doencas)

        # Escolher clínica ou UPA baseada na gravidade da doença
        clinica = escolher_clinica(doenca, clinicas_publicas, clinicas_privadas)
        if not clinica:
            logging.warning(f"Capacidade excedida para o paciente {paciente.nome}, agendando para outro dia.")
            gerar_agendamento(session, paciente, clinica, doenca, "Capacidade excedida")
            continue

        # Selecionar médico disponível
        medico = selecionar_medico(paciente, doenca, medicos)
        if not medico:
            logging.warning(f"Falta de médico para o paciente {paciente.nome}, reagendando.")
            gerar_agendamento(session, paciente, clinica, doenca, "Falta de médico")
            continue

        # Definir horários do atendimento
        hora_atendimento = fake.time_object()
        hora_conclusao = (datetime.combine(datetime.today(), hora_atendimento) + timedelta(minutes=random.randint(15, 120))).time()

        # Verificar o status de acordo com o ano
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
        session.add(atendimento)
        session.flush()  # Garantir que o atendimento foi salvo e o ID foi gerado

        # Criar prontuário vinculado ao atendimento gerado
        prontuario = Prontuario(
            id_paciente=paciente.id,
            id_atendimento=atendimento.id,  # Usar o ID do atendimento gerado
            id_medico=medico.id,
            descricao=fake.text(),
            data=data_atendimento.date(),
            hora=hora_atendimento,
            status_conclusao=gerar_status_conclusao(doenca, clinica, bairro, taxa_mortalidade_bairros[bairro.id])
        )
        prontuarios_batch.append(prontuario)

        atendimentos_gerados += 1

        # Commit a cada 1000 atendimentos para otimização
        if atendimentos_gerados % 1000 == 0:
            session.bulk_save_objects(atendimentos_batch)
            session.bulk_save_objects(prontuarios_batch)
            session.commit()
            atendimentos_batch.clear()
            prontuarios_batch.clear()

    # Commit dos atendimentos e prontuários restantes
    session.bulk_save_objects(prontuarios_batch)
    session.commit()

    logging.info(f"{atendimentos_gerados} atendimentos foram gerados com sucesso.")

# Funções auxiliares
def escolher_clinica(doenca, clinicas_publicas, clinicas_privadas):
    """Escolhe a clínica adequada com base na gravidade da doença."""
    if doenca.gravidade in ['Muito Grave', 'Grave']:
        return next((c for c in clinicas_publicas if 'UPA' in c.nome), None) or random.choice(clinicas_publicas)
    elif doenca.gravidade == 'Moderada':
        return next((c for c in clinicas_publicas if 'Centro de Saúde' in c.nome), None) or random.choice(clinicas_privadas)
    return random.choice(clinicas_privadas)

def selecionar_medico(paciente, doenca, medicos):
    """Seleciona o médico adequado para o atendimento."""
    if doenca.requer_cirurgia:
        return next((m for m in medicos if m.especialidade == doenca.especialista), None) or random.choice(medicos)
    if paciente.idade <= 12:
        return next((m for m in medicos if m.especialidade == 'Pediatria'), None) or random.choice(medicos)
    return next((m for m in medicos if m.especialidade == 'Clínico Geral'), None) or random.choice(medicos)

def gerar_status_conclusao(doenca, clinica, bairro, taxa_mortalidade):
    """Define o status de conclusão do prontuário com base na doença, local de atendimento e mortalidade."""
    if doenca.requer_cirurgia and 'UPA' in clinica.nome:
        return 'Encaminhado para hospital'

    # Probabilidade de óbito
    if random.random() < taxa_mortalidade:
        return 'Óbito'
    
    return random.choice(['Curado', 'Em tratamento', 'Sem retorno'])

def validar_ano_atendimento(data_atendimento):
    """Valida o status do atendimento com base no ano."""
    ano = data_atendimento.year
    if ano in [2022, 2023]:
        return 'Concluído'
    elif ano == 2024:
        return random.choice(['Concluído', 'Em andamento', 'Cancelado', 'Aguardando'])
    return 'Concluído'