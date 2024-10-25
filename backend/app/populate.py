# app/populate.py
import logging

from pytest import Session
from .models import Base, Doenca, Bairro, Paciente, Clinica, Medico, ProfissionalSaude
from faker import Faker
import random

fake = Faker('pt_BR')

def reset_database(session: Session) -> None:
    """Função para limpar as tabelas e resetar o banco de dados antes de inserir novos dados."""
    meta = Base.metadata  # Acessa o metadata do Base
    for table in reversed(meta.sorted_tables):
        session.execute(table.delete())
    session.commit()

class Doenca:
    def __init__(self, nome, especialista, sintomas, requer_cirurgia, gravidade):
        self.nome = nome
        self.especialista = especialista
        self.sintomas = sintomas
        self.requer_cirurgia = requer_cirurgia
        self.gravidade = gravidade

class Especialidade:
    def __init__(self, nome):
        self.nome = nome
        self.doencas = []

    def adicionar_doenca(self, doenca):
        self.doencas.append(doenca)

    def filtrar_doencas(self, requer_cirurgia=None, gravidade=None):
        return [
            doenca for doenca in self.doencas
            if (requer_cirurgia is None or doenca.requer_cirurgia == requer_cirurgia) and
               (gravidade is None or doenca.gravidade == gravidade)
        ]

# Criando especialidades e adicionando doenças
especialidades = {
    "Clínico Geral": Especialidade("Clínico Geral"),
    "Pediatra": Especialidade("Pediatra"),
    "Cardiologista": Especialidade("Cardiologista"),
    "Ortopedista": Especialidade("Ortopedista"),
    "Neurologista": Especialidade("Neurologista"),
    "Dermatologista": Especialidade("Dermatologista"),
    "Gastroenterologista": Especialidade("Gastroenterologista"),
    "Oftalmologista": Especialidade("Oftalmologista"),
    "Psiquiatra": Especialidade("Psiquiatra"),
    "Endocrinologista": Especialidade("Endocrinologista")
}

# Lista de doenças por especialidade
doencas = [
    # Exemplo de instância
    Doenca('Gripe', 'Clínico Geral', ['febre', 'dor no corpo', 'tosse'], False, 'Leve'),
    Doenca('Pneumonia', 'Clínico Geral', ['tosse', 'febre alta', 'dor no peito'], False, 'Grave'),
    Doenca('Dengue', 'Clínico Geral', ['febre alta', 'dores musculares', 'manchas na pele'], False, 'Grave'),
    Doenca('Bronquite', 'Clínico Geral', ['tosse', 'falta de ar', 'fadiga'], False, 'Moderada'),
    Doenca('Sinusite', 'Clínico Geral', ['dor facial', 'congestão nasal', 'tosse'], False, 'Leve'),
    
    Doenca('Otite Média', 'Pediatra', ['dor de ouvido', 'febre', 'irritabilidade'], False, 'Moderada'),
    Doenca('Amigdalite', 'Pediatra', ['dor de garganta', 'dificuldade para engolir', 'febre'], False, 'Leve'),
    Doenca('Varicela (Catapora)', 'Pediatra', ['erupções cutâneas', 'febre', 'coceira'], False, 'Leve'),
    Doenca('Escarlatina', 'Pediatra', ['erupção vermelha', 'dor de garganta', 'febre alta'], False, 'Grave'),
    Doenca('Asma', 'Pediatra', ['falta de ar', 'tosse', 'chiado no peito'], False, 'Moderada'),
    
    Doenca('Infarto do Miocárdio', 'Cardiologista', ['dor no peito', 'falta de ar', 'suor'], True, 'Muito Grave'),
    Doenca('Arritmia Cardíaca', 'Cardiologista', ['palpitações', 'tontura', 'fadiga'], True, 'Grave'),
    Doenca('Hipertensão Arterial', 'Cardiologista', ['dor de cabeça', 'fadiga', 'tontura'], False, 'Moderada'),
    Doenca('Insuficiência Cardíaca', 'Cardiologista', ['falta de ar', 'inchaço nas pernas', 'fadiga'], False, 'Grave'),
    Doenca('Endocardite', 'Cardiologista', ['febre', 'dor no peito', 'cansaço'], True, 'Muito Grave'),
    
    Doenca('Fratura Óssea', 'Ortopedista', ['dor intensa', 'inchaço', 'deformidade'], True, 'Muito Grave'),
    Doenca('Entorse de Tornozelo', 'Ortopedista', ['dor', 'inchaço', 'dificuldade para caminhar'], False, 'Moderada'),
    Doenca('Escoliose', 'Ortopedista', ['desalinhamento da coluna', 'dor nas costas'], True, 'Grave'),
    Doenca('Hérnia de Disco', 'Ortopedista', ['dor nas costas', 'formigamento nas pernas'], True, 'Grave'),
    Doenca('Luxação', 'Ortopedista', ['dor intensa', 'inchaço', 'deformidade'], True, 'Grave'),

    Doenca('Epilepsia', 'Neurologista', ['convulsões', 'perda de consciência', 'espasmos musculares'], False, 'Moderada'),
    Doenca('Enxaqueca', 'Neurologista', ['dor de cabeça intensa', 'náusea', 'sensibilidade à luz'], False, 'Moderada'),
    Doenca('Parkinson', 'Neurologista', ['tremores', 'rigidez muscular', 'dificuldade para se mover'], False, 'Grave'),
    Doenca('Alzheimer', 'Neurologista', ['perda de memória', 'confusão mental', 'dificuldade para realizar tarefas'], False, 'Muito Grave'),
    Doenca('AVC (Acidente Vascular Cerebral)', 'Neurologista', ['fraqueza de um lado do corpo', 'confusão', 'perda de fala'], True, 'Muito Grave'),

    # Especialidades Privadas
    Doenca('Psoríase', 'Dermatologista', ['manchas vermelhas na pele', 'coceira', 'descamação'], False, 'Moderada'),
    Doenca('Acne', 'Dermatologista', ['espinhas', 'cravos', 'vermelhidão na pele'], False, 'Leve'),
    Doenca('Melanoma', 'Dermatologista', ['manchas escuras na pele', 'mudança de cor', 'sangramento'], True, 'Muito Grave'),
    Doenca('Dermatite Atópica', 'Dermatologista', ['coceira', 'vermelhidão', 'rachaduras na pele'], False, 'Moderada'),
    Doenca('Vitiligo', 'Dermatologista', ['perda de pigmentação', 'manchas brancas na pele'], False, 'Leve'),

    Doenca('Gastrite', 'Gastroenterologista', ['dor abdominal', 'azia', 'náusea'], False, 'Moderada'),
    Doenca('Úlcera Péptica', 'Gastroenterologista', ['dor abdominal', 'sangramento', 'indigestão'], True, 'Grave'),
    Doenca('Doença de Crohn', 'Gastroenterologista', ['dor abdominal', 'diarreia', 'perda de peso'], True, 'Grave'),
    Doenca('Hepatite', 'Gastroenterologista', ['fadiga', 'pele amarelada', 'náusea'], False, 'Grave'),
    Doenca('Síndrome do Intestino Irritável', 'Gastroenterologista', ['dor abdominal', 'diarreia', 'inchaço'], False, 'Moderada'),

    Doenca('Miopia', 'Oftalmologista', ['visão borrada à distância'], False, 'Leve'),
    Doenca('Catarata', 'Oftalmologista', ['visão embaçada', 'sensibilidade à luz'], True, 'Grave'),
    Doenca('Glaucoma', 'Oftalmologista', ['perda de visão', 'dor ocular', 'ver halos ao redor de luzes'], True, 'Grave'),
    Doenca('Descolamento de Retina', 'Oftalmologista', ['perda súbita de visão', 'flashes de luz', 'moscas volantes'], True, 'Muito Grave'),
    Doenca('Conjuntivite', 'Oftalmologista', ['vermelhidão ocular', 'coceira', 'lacrimejamento'], False, 'Leve'),

    Doenca('Depressão', 'Psiquiatra', ['tristeza persistente', 'fadiga', 'falta de interesse'], False, 'Moderada'),
    Doenca('Transtorno de Ansiedade', 'Psiquiatra', ['preocupação excessiva', 'insônia', 'tensão muscular'], False, 'Moderada'),
    Doenca('Transtorno Bipolar', 'Psiquiatra', ['mudanças de humor', 'comportamento impulsivo', 'depressão'], False, 'Grave'),
    Doenca('Esquizofrenia', 'Psiquiatra', ['alucinações', 'delírios', 'isolamento social'], False, 'Muito Grave'),
    Doenca('Transtorno de Estresse Pós-Traumático (TEPT)', 'Psiquiatra', ['flashbacks', 'ansiedade', 'insônia'], False, 'Moderada'),

    Doenca('Diabetes Tipo 1', 'Endocrinologista', ['sede excessiva', 'perda de peso', 'fadiga'], False, 'Grave'),
    Doenca('Diabetes Tipo 2', 'Endocrinologista', ['sede excessiva', 'fadiga', 'visão embaçada'], False, 'Moderada'),
    Doenca('Hipotireoidismo', 'Endocrinologista', ['fadiga', 'aumento de peso', 'sensibilidade ao frio'], False, 'Moderada'),
    Doenca('Hipertireoidismo', 'Endocrinologista', ['perda de peso', 'ansiedade', 'insônia'], False, 'Moderada'),
    Doenca('Síndrome de Cushing', 'Endocrinologista', ['ganho de peso', 'rosto arredondado', 'fraqueza muscular'], True, 'Grave')
]

# Adicionando as doenças às especialidades correspondentes
for doenca in doencas:
    especialidades[doenca.especialista].adicionar_doenca(doenca)

# Exemplo de filtragem por doenças que requerem cirurgia e são de gravidade 'Grave' na especialidade 'Cardiologista'
doencas_filtradas = especialidades['Cardiologista'].filtrar_doencas(requer_cirurgia=True, gravidade='Grave')
for doenca in doencas_filtradas:
    print(f"Doença: {doenca.nome}, Gravidade: {doenca.gravidade}")


def populate_doencas(session):
    """Popula doenças no banco de dados."""
    session.add_all(doencas)
    session.commit()

def populate_bairros(session):
    """Popula bairros no banco de dados."""
    bairros = [
        Bairro(nome='Santa Tereza', pop_total=22808, infra_saude='1 centro de saúde, 1 UPA, 2 clínicas particulares'),
        Bairro(nome='Horto', pop_total=4360, infra_saude='1 centro de saúde, 1 UPA, 2 clínicas particulares')
    ]
    session.add_all(bairros)
    session.commit()

def populate_pacientes(session, total_populacao):
    """Popula pacientes no banco de dados."""
    pacientes = [
        Paciente(
            nome=fake.name(),
            idade=fake.random_int(min=1, max=100),
            sexo=fake.random_element(elements=('M', 'F')),
            endereco=fake.address(),
            telefone=fake.phone_number()
        )
        for _ in range(total_populacao)
    ]
    session.add_all(pacientes)
    session.commit()

def populate_clinicas(session):
    """Popula clínicas no banco de dados."""
    clinicas = [
        Clinica(nome='UPA Santa Tereza', tipo='Pública', capacidade_diaria=300, capacidade_leito=50, endereco='Rua A, 111'),
        Clinica(nome='Centro de Saúde Horto', tipo='Pública', capacidade_diaria=200, capacidade_leito=20, endereco='Rua B, 222'),
        Clinica(nome='Clínica Particular 1', tipo='Privada', capacidade_diaria=50, capacidade_leito=0, endereco='Rua C, 333'),
        Clinica(nome='Clínica Particular 2', tipo='Privada', capacidade_diaria=30, capacidade_leito=0, endereco='Av. D, 444')
    ]
    session.add_all(clinicas)
    session.commit()

def add_medicos(clinica, medicos, qtd_clinicos, qtd_especialistas, especialidades):
    """Adiciona médicos para uma clínica."""
    medicos += [
        Medico(nome=fake.name(), especialidade='Clínico Geral', crm=fake.numerify(text='####/##'))
        for _ in range(qtd_clinicos)
    ]
    medicos += [
        Medico(nome=fake.name(), especialidade=random.choice(especialidades), crm=fake.numerify(text='####/##'))
        for _ in range(qtd_especialistas)
    ]

def populate_medicos(session):
    """Popula médicos no banco de dados, separando por público e privado."""
    medicos = []
    clinicas = session.query(Clinica).all()

    for clinica in clinicas:
        if clinica.tipo == 'Pública':
            if 'UPA' in clinica.nome:
                # UPA: 10 clínicos gerais, 5 especialistas
                add_medicos(clinica, medicos, 10, 5, especialidades_publico)
            elif 'Centro de Saúde' in clinica.nome:
                # Centro de Saúde: 4 clínicos gerais, 1 pediatra
                add_medicos(clinica, medicos, 4, 1, ['Pediatria'])
        else:
            # Clínicas privadas: 5 especialistas por clínica, escolhidos aleatoriamente entre especialidades privadas
            add_medicos(clinica, medicos, 0, 5, especialidades_privado)

    session.add_all(medicos)
    session.commit()

def populate_profissionais_saude(session):
    """Popula profissionais de saúde (enfermeiros e técnicos de enfermagem)."""
    profissionais = [
        ProfissionalSaude(nome=fake.name(), tipo=random.choice(['Enfermeiro', 'Técnico de Enfermagem']))
        for _ in range(25)  # 15 enfermeiros e 10 técnicos
    ]
    session.add_all(profissionais)
    session.commit()

def populate_data(session):
    """Popula o banco de dados com dados fictícios e reais baseados nos requisitos."""
    
    # Limpar tabelas antes da inserção para evitar duplicidade em testes contínuos
    reset_database(session)

    logging.info("Populando doenças...")
    populate_doencas(session)
    
    logging.info("Populando bairros...")
    populate_bairros(session)
    
    total_populacao = sum(bairro.pop_total for bairro in session.query(Bairro).all())
    logging.info(f"Populando pacientes para {total_populacao} pessoas...")
    populate_pacientes(session, total_populacao)
    
    logging.info("Populando clínicas...")
    populate_clinicas(session)
    
    logging.info("Populando médicos...")
    populate_medicos(session)
    
    logging.info("Populando profissionais de saúde...")
    populate_profissionais_saude(session)
    
    logging.info("População de dados concluída com sucesso!")
