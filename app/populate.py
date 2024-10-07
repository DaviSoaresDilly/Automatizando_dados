# app/populate.py
from app.models import Doenca, Bairro, Paciente, Clinica, Medico, ProfissionalSaude
from faker import Faker
import random

fake = Faker('pt_BR')

# Listas reais de especialidades médicas e doenças com cirurgia
especialidades_publico = ['Clínico Geral', 'Pediatria', 'Cardiologia', 'Ortopedia', 'Neurologia']
especialidades_privado = ['Dermatologia', 'Gastroenterologia', 'Oftalmologia', 'Psiquiatria', 'Endocrinologia']

# Lista de doenças por especialidade pública e privada
doencas_reais = [
    # Especialidades Públicas
    {'nome': 'Gripe', 'especialista': 'Clínico Geral', 'sintomas': ['febre', 'dor no corpo', 'tosse'], 'requer_cirurgia': False, 'gravidade': 'Leve'},
    {'nome': 'Pneumonia', 'especialista': 'Clínico Geral', 'sintomas': ['tosse', 'febre alta', 'dor no peito'], 'requer_cirurgia': False, 'gravidade': 'Grave'},
    {'nome': 'Dengue', 'especialista': 'Clínico Geral', 'sintomas': ['febre alta', 'dores musculares', 'manchas na pele'], 'requer_cirurgia': False, 'gravidade': 'Grave'},
    {'nome': 'Bronquite', 'especialista': 'Clínico Geral', 'sintomas': ['tosse', 'falta de ar', 'fadiga'], 'requer_cirurgia': False, 'gravidade': 'Moderada'},
    {'nome': 'Sinusite', 'especialista': 'Clínico Geral', 'sintomas': ['dor facial', 'congestão nasal', 'tosse'], 'requer_cirurgia': False, 'gravidade': 'Leve'},
    
    {'nome': 'Otite Média', 'especialista': 'Pediatra', 'sintomas': ['dor de ouvido', 'febre', 'irritabilidade'], 'requer_cirurgia': False, 'gravidade': 'Moderada'},
    {'nome': 'Amigdalite', 'especialista': 'Pediatra', 'sintomas': ['dor de garganta', 'dificuldade para engolir', 'febre'], 'requer_cirurgia': False, 'gravidade': 'Leve'},
    {'nome': 'Varicela (Catapora)', 'especialista': 'Pediatra', 'sintomas': ['erupções cutâneas', 'febre', 'coceira'], 'requer_cirurgia': False, 'gravidade': 'Leve'},
    {'nome': 'Escarlatina', 'especialista': 'Pediatra', 'sintomas': ['erupção vermelha', 'dor de garganta', 'febre alta'], 'requer_cirurgia': False, 'gravidade': 'Grave'},
    {'nome': 'Asma', 'especialista': 'Pediatra', 'sintomas': ['falta de ar', 'tosse', 'chiado no peito'], 'requer_cirurgia': False, 'gravidade': 'Moderada'},
    
    {'nome': 'Infarto do Miocárdio', 'especialista': 'Cardiologista', 'sintomas': ['dor no peito', 'falta de ar', 'suor'], 'requer_cirurgia': True, 'gravidade': 'Muito Grave'},
    {'nome': 'Arritmia Cardíaca', 'especialista': 'Cardiologista', 'sintomas': ['palpitações', 'tontura', 'fadiga'], 'requer_cirurgia': True, 'gravidade': 'Grave'},
    {'nome': 'Hipertensão Arterial', 'especialista': 'Cardiologista', 'sintomas': ['dor de cabeça', 'fadiga', 'tontura'], 'requer_cirurgia': False, 'gravidade': 'Moderada'},
    {'nome': 'Insuficiência Cardíaca', 'especialista': 'Cardiologista', 'sintomas': ['falta de ar', 'inchaço nas pernas', 'fadiga'], 'requer_cirurgia': False, 'gravidade': 'Grave'},
    {'nome': 'Endocardite', 'especialista': 'Cardiologista', 'sintomas': ['febre', 'dor no peito', 'cansaço'], 'requer_cirurgia': True, 'gravidade': 'Muito Grave'},
    
    {'nome': 'Fratura Óssea', 'especialista': 'Ortopedista', 'sintomas': ['dor intensa', 'inchaço', 'deformidade'], 'requer_cirurgia': True, 'gravidade': 'Muito Grave'},
    {'nome': 'Entorse de Tornozelo', 'especialista': 'Ortopedista', 'sintomas': ['dor', 'inchaço', 'dificuldade para caminhar'], 'requer_cirurgia': False, 'gravidade': 'Moderada'},
    {'nome': 'Escoliose', 'especialista': 'Ortopedista', 'sintomas': ['desalinhamento da coluna', 'dor nas costas'], 'requer_cirurgia': True, 'gravidade': 'Grave'},
    {'nome': 'Hérnia de Disco', 'especialista': 'Ortopedista', 'sintomas': ['dor nas costas', 'formigamento nas pernas'], 'requer_cirurgia': True, 'gravidade': 'Grave'},
    {'nome': 'Luxação', 'especialista': 'Ortopedista', 'sintomas': ['dor intensa', 'inchaço', 'deformidade'], 'requer_cirurgia': True, 'gravidade': 'Grave'},

    {'nome': 'Epilepsia', 'especialista': 'Neurologista', 'sintomas': ['convulsões', 'perda de consciência', 'espasmos musculares'], 'requer_cirurgia': False, 'gravidade': 'Moderada'},
    {'nome': 'Enxaqueca', 'especialista': 'Neurologista', 'sintomas': ['dor de cabeça intensa', 'náusea', 'sensibilidade à luz'], 'requer_cirurgia': False, 'gravidade': 'Moderada'},
    {'nome': 'Parkinson', 'especialista': 'Neurologista', 'sintomas': ['tremores', 'rigidez muscular', 'dificuldade para se mover'], 'requer_cirurgia': False, 'gravidade': 'Grave'},
    {'nome': 'Alzheimer', 'especialista': 'Neurologista', 'sintomas': ['perda de memória', 'confusão mental', 'dificuldade para realizar tarefas'], 'requer_cirurgia': False, 'gravidade': 'Muito Grave'},
    {'nome': 'AVC (Acidente Vascular Cerebral)', 'especialista': 'Neurologista', 'sintomas': ['fraqueza de um lado do corpo', 'confusão', 'perda de fala'], 'requer_cirurgia': True, 'gravidade': 'Muito Grave'},

    # Especialidades Privadas
    {'nome': 'Psoríase', 'especialista': 'Dermatologista', 'sintomas': ['manchas vermelhas na pele', 'coceira', 'descamação'], 'requer_cirurgia': False, 'gravidade': 'Moderada'},
    {'nome': 'Acne', 'especialista': 'Dermatologista', 'sintomas': ['espinhas', 'cravos', 'vermelhidão na pele'], 'requer_cirurgia': False, 'gravidade': 'Leve'},
    {'nome': 'Melanoma', 'especialista': 'Dermatologista', 'sintomas': ['manchas escuras na pele', 'mudança de cor', 'sangramento'], 'requer_cirurgia': True, 'gravidade': 'Muito Grave'},
    {'nome': 'Dermatite Atópica', 'especialista': 'Dermatologista', 'sintomas': ['coceira', 'vermelhidão', 'rachaduras na pele'], 'requer_cirurgia': False, 'gravidade': 'Moderada'},
    {'nome': 'Vitiligo', 'especialista': 'Dermatologista', 'sintomas': ['perda de pigmentação', 'manchas brancas na pele'], 'requer_cirurgia': False, 'gravidade': 'Leve'},

    {'nome': 'Gastrite', 'especialista': 'Gastroenterologista', 'sintomas': ['dor abdominal', 'azia', 'náusea'], 'requer_cirurgia': False, 'gravidade': 'Moderada'},
    {'nome': 'Úlcera Péptica', 'especialista': 'Gastroenterologista', 'sintomas': ['dor abdominal', 'sangramento', 'indigestão'], 'requer_cirurgia': True, 'gravidade': 'Grave'},
    {'nome': 'Doença de Crohn', 'especialista': 'Gastroenterologista', 'sintomas': ['dor abdominal', 'diarreia', 'perda de peso'], 'requer_cirurgia': True, 'gravidade': 'Grave'},
    {'nome': 'Hepatite', 'especialista': 'Gastroenterologista', 'sintomas': ['fadiga', 'pele amarelada', 'náusea'], 'requer_cirurgia': False, 'gravidade': 'Grave'},
    {'nome': 'Síndrome do Intestino Irritável', 'especialista': 'Gastroenterologista', 'sintomas': ['dor abdominal', 'diarreia', 'inchaço'], 'requer_cirurgia': False, 'gravidade': 'Moderada'},

    {'nome': 'Miopia', 'especialista': 'Oftalmologista', 'sintomas': ['visão borrada à distância'], 'requer_cirurgia': False, 'gravidade': 'Leve'},
    {'nome': 'Catarata', 'especialista': 'Oftalmologista', 'sintomas': ['visão embaçada', 'sensibilidade à luz'], 'requer_cirurgia': True, 'gravidade': 'Grave'},
    {'nome': 'Glaucoma', 'especialista': 'Oftalmologista', 'sintomas': ['perda de visão', 'dor ocular', 'ver halos ao redor de luzes'], 'requer_cirurgia': True, 'gravidade': 'Grave'},
    {'nome': 'Descolamento de Retina', 'especialista': 'Oftalmologista', 'sintomas': ['perda súbita de visão', 'flashes de luz', 'moscas volantes'], 'requer_cirurgia': True, 'gravidade': 'Muito Grave'},
    {'nome': 'Conjuntivite', 'especialista': 'Oftalmologista', 'sintomas': ['vermelhidão ocular', 'coceira', 'lacrimejamento'], 'requer_cirurgia': False, 'gravidade': 'Leve'},

    {'nome': 'Depressão', 'especialista': 'Psiquiatra', 'sintomas': ['tristeza persistente', 'fadiga', 'falta de interesse'], 'requer_cirurgia': False, 'gravidade': 'Moderada'},
    {'nome': 'Transtorno de Ansiedade', 'especialista': 'Psiquiatra', 'sintomas': ['preocupação excessiva', 'insônia', 'tensão muscular'], 'requer_cirurgia': False, 'gravidade': 'Moderada'},
    {'nome': 'Transtorno Bipolar', 'especialista': 'Psiquiatra', 'sintomas': ['mudanças de humor', 'comportamento impulsivo', 'depressão'], 'requer_cirurgia': False, 'gravidade': 'Grave'},
    {'nome': 'Esquizofrenia', 'especialista': 'Psiquiatra', 'sintomas': ['alucinações', 'delírios', 'isolamento social'], 'requer_cirurgia': False, 'gravidade': 'Muito Grave'},
    {'nome': 'Transtorno de Estresse Pós-Traumático (TEPT)', 'especialista': 'Psiquiatra', 'sintomas': ['flashbacks', 'ansiedade', 'insônia'], 'requer_cirurgia': False, 'gravidade': 'Moderada'},

    {'nome': 'Diabetes Tipo 1', 'especialista': 'Endocrinologista', 'sintomas': ['sede excessiva', 'perda de peso', 'fadiga'], 'requer_cirurgia': False, 'gravidade': 'Grave'},
    {'nome': 'Diabetes Tipo 2', 'especialista': 'Endocrinologista', 'sintomas': ['sede excessiva', 'fadiga', 'visão embaçada'], 'requer_cirurgia': False, 'gravidade': 'Moderada'},
    {'nome': 'Hipotireoidismo', 'especialista': 'Endocrinologista', 'sintomas': ['fadiga', 'aumento de peso', 'sensibilidade ao frio'], 'requer_cirurgia': False, 'gravidade': 'Moderada'},
    {'nome': 'Hipertireoidismo', 'especialista': 'Endocrinologista', 'sintomas': ['perda de peso', 'ansiedade', 'insônia'], 'requer_cirurgia': False, 'gravidade': 'Moderada'},
    {'nome': 'Síndrome de Cushing', 'especialista': 'Endocrinologista', 'sintomas': ['ganho de peso', 'rosto arredondado', 'fraqueza muscular'], 'requer_cirurgia': True, 'gravidade': 'Grave'}
]

def populate_doencas(session):
    """Popula doenças no banco de dados."""
    doencas = [
        Doenca(
            nome=doenca['nome'],
            especialista=doenca['especialista'],
            sintomas=', '.join(doenca['sintomas']),
            gravidade=doenca['gravidade'],
            requer_cirurgia=doenca['requer_cirurgia']
        )
        for doenca in doencas_reais
    ]
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
            # Clínicas privadas: 5 especialistas por clínica
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
    populate_doencas(session)
    populate_bairros(session)
    
    total_populacao = sum(bairro.pop_total for bairro in session.query(Bairro).all())
    populate_pacientes(session, total_populacao)
    
    populate_clinicas(session)
    populate_medicos(session)
    populate_profissionais_saude(session)
    
    print("População de dados concluída com sucesso!")