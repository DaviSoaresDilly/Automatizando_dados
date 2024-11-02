# app/populate.py
from datetime import timedelta
import logging
from .models import (
    Agendamento,
    AtendimentoProfissional,
    AtendimentoPulado,
    Base,
    Doenca,
    Bairro,
    Paciente,
    Clinica,
    Medico,
    ProfissionalSaude,
)
from faker import Faker
import random
import json

fake = Faker("pt_BR")

# Configuração de logging detalhado
logging.basicConfig(level=logging.INFO)


# Função para resetar o banco de dados
def reset_database(session):
    """Função para limpar as tabelas e resetar o banco de dados antes de inserir novos dados."""
    meta = Base.metadata
    for table in reversed(meta.sorted_tables):
        session.execute(table.delete())
    session.commit()


# Definição de classes para especialidades e doenças
class Especialidade:
    def __init__(self, nome):
        self.nome = nome
        self.doencas = []

    def adicionar_doenca(self, doenca):
        self.doencas.append(doenca)

    def filtrar_doencas(self, requer_cirurgia=None, gravidade=None):
        return [
            doenca
            for doenca in self.doencas
            if (requer_cirurgia is None or doenca.requer_cirurgia == requer_cirurgia)
            and (gravidade is None or doenca.gravidade == gravidade)
        ]


# Lista de especialidades para médicos que atendem em clínicas públicas
especialidades_publico = [
    "Pediatria",
    "Cardiologia",
    "Ortopedia",
    "Ginecologia",
    "Dermatologia",
]
# Lista de especialidades para médicos que atendem em clínicas privadas
especialidades_privado = [
    "Oftalmologia",
    "Neurologia",
    "Gastroenterologia",
    "Psiquiatria",
    "Endocrinologia",
]


# Exemplo de filtragem de doenças por especialidade
def populate_doencas(session):
    # Lista de doenças por especialidade
    doencas = [
        # Exemplo de instância
        Doenca(
            "Gripe", "Clínico Geral", ["febre", "dor no corpo", "tosse"], False, "Leve"
        ),
        Doenca(
            "Pneumonia",
            "Clínico Geral",
            ["tosse", "febre alta", "dor no peito"],
            False,
            "Grave",
        ),
        Doenca(
            "Dengue",
            "Clínico Geral",
            ["febre alta", "dores musculares", "manchas na pele"],
            False,
            "Grave",
        ),
        Doenca(
            "Bronquite",
            "Clínico Geral",
            ["tosse", "falta de ar", "fadiga"],
            False,
            "Moderada",
        ),
        Doenca(
            "Sinusite",
            "Clínico Geral",
            ["dor facial", "congestão nasal", "tosse"],
            False,
            "Leve",
        ),
        Doenca(
            "Otite Média",
            "Pediatra",
            ["dor de ouvido", "febre", "irritabilidade"],
            False,
            "Moderada",
        ),
        Doenca(
            "Amigdalite",
            "Pediatra",
            ["dor de garganta", "dificuldade para engolir", "febre"],
            False,
            "Leve",
        ),
        Doenca(
            "Varicela (Catapora)",
            "Pediatra",
            ["erupções cutâneas", "febre", "coceira"],
            False,
            "Leve",
        ),
        Doenca(
            "Escarlatina",
            "Pediatra",
            ["erupção vermelha", "dor de garganta", "febre alta"],
            False,
            "Grave",
        ),
        Doenca(
            "Asma",
            "Pediatra",
            ["falta de ar", "tosse", "chiado no peito"],
            False,
            "Moderada",
        ),
        Doenca(
            "Infarto do Miocárdio",
            "Cardiologista",
            ["dor no peito", "falta de ar", "suor"],
            True,
            "Muito Grave",
        ),
        Doenca(
            "Arritmia Cardíaca",
            "Cardiologista",
            ["palpitações", "tontura", "fadiga"],
            True,
            "Grave",
        ),
        Doenca(
            "Hipertensão Arterial",
            "Cardiologista",
            ["dor de cabeça", "fadiga", "tontura"],
            False,
            "Moderada",
        ),
        Doenca(
            "Insuficiência Cardíaca",
            "Cardiologista",
            ["falta de ar", "inchaço nas pernas", "fadiga"],
            False,
            "Grave",
        ),
        Doenca(
            "Endocardite",
            "Cardiologista",
            ["febre", "dor no peito", "cansaço"],
            True,
            "Muito Grave",
        ),
        Doenca(
            "Fratura Óssea",
            "Ortopedista",
            ["dor intensa", "inchaço", "deformidade"],
            True,
            "Muito Grave",
        ),
        Doenca(
            "Entorse de Tornozelo",
            "Ortopedista",
            ["dor", "inchaço", "dificuldade para caminhar"],
            False,
            "Moderada",
        ),
        Doenca(
            "Escoliose",
            "Ortopedista",
            ["desalinhamento da coluna", "dor nas costas"],
            True,
            "Grave",
        ),
        Doenca(
            "Hérnia de Disco",
            "Ortopedista",
            ["dor nas costas", "formigamento nas pernas"],
            True,
            "Grave",
        ),
        Doenca(
            "Luxação",
            "Ortopedista",
            ["dor intensa", "inchaço", "deformidade"],
            True,
            "Grave",
        ),
        Doenca(
            "Epilepsia",
            "Neurologista",
            ["convulsões", "perda de consciência", "espasmos musculares"],
            False,
            "Moderada",
        ),
        Doenca(
            "Enxaqueca",
            "Neurologista",
            ["dor de cabeça intensa", "náusea", "sensibilidade à luz"],
            False,
            "Moderada",
        ),
        Doenca(
            "Parkinson",
            "Neurologista",
            ["tremores", "rigidez muscular", "dificuldade para se mover"],
            False,
            "Grave",
        ),
        Doenca(
            "Alzheimer",
            "Neurologista",
            [
                "perda de memória",
                "confusão mental",
                "dificuldade para realizar tarefas",
            ],
            False,
            "Muito Grave",
        ),
        Doenca(
            "AVC (Acidente Vascular Cerebral)",
            "Neurologista",
            ["fraqueza de um lado do corpo", "confusão", "perda de fala"],
            True,
            "Muito Grave",
        ),
        # Especialidades Privadas
        Doenca(
            "Psoríase",
            "Dermatologista",
            ["manchas vermelhas na pele", "coceira", "descamação"],
            False,
            "Moderada",
        ),
        Doenca(
            "Acne",
            "Dermatologista",
            ["espinhas", "cravos", "vermelhidão na pele"],
            False,
            "Leve",
        ),
        Doenca(
            "Melanoma",
            "Dermatologista",
            ["manchas escuras na pele", "mudança de cor", "sangramento"],
            True,
            "Muito Grave",
        ),
        Doenca(
            "Dermatite Atópica",
            "Dermatologista",
            ["coceira", "vermelhidão", "rachaduras na pele"],
            False,
            "Moderada",
        ),
        Doenca(
            "Vitiligo",
            "Dermatologista",
            ["perda de pigmentação", "manchas brancas na pele"],
            False,
            "Leve",
        ),
        Doenca(
            "Gastrite",
            "Gastroenterologista",
            ["dor abdominal", "azia", "náusea"],
            False,
            "Moderada",
        ),
        Doenca(
            "Úlcera Péptica",
            "Gastroenterologista",
            ["dor abdominal", "sangramento", "indigestão"],
            True,
            "Grave",
        ),
        Doenca(
            "Doença de Crohn",
            "Gastroenterologista",
            ["dor abdominal", "diarreia", "perda de peso"],
            True,
            "Grave",
        ),
        Doenca(
            "Hepatite",
            "Gastroenterologista",
            ["fadiga", "pele amarelada", "náusea"],
            False,
            "Grave",
        ),
        Doenca(
            "Síndrome do Intestino Irritável",
            "Gastroenterologista",
            ["dor abdominal", "diarreia", "inchaço"],
            False,
            "Moderada",
        ),
        Doenca(
            "Miopia", "Oftalmologista", ["visão borrada à distância"], False, "Leve"
        ),
        Doenca(
            "Catarata",
            "Oftalmologista",
            ["visão embaçada", "sensibilidade à luz"],
            True,
            "Grave",
        ),
        Doenca(
            "Glaucoma",
            "Oftalmologista",
            ["perda de visão", "dor ocular", "ver halos ao redor de luzes"],
            True,
            "Grave",
        ),
        Doenca(
            "Descolamento de Retina",
            "Oftalmologista",
            ["perda súbita de visão", "flashes de luz", "moscas volantes"],
            True,
            "Muito Grave",
        ),
        Doenca(
            "Conjuntivite",
            "Oftalmologista",
            ["vermelhidão ocular", "coceira", "lacrimejamento"],
            False,
            "Leve",
        ),
        Doenca(
            "Depressão",
            "Psiquiatra",
            ["tristeza persistente", "fadiga", "falta de interesse"],
            False,
            "Moderada",
        ),
        Doenca(
            "Transtorno de Ansiedade",
            "Psiquiatra",
            ["preocupação excessiva", "insônia", "tensão muscular"],
            False,
            "Moderada",
        ),
        Doenca(
            "Transtorno Bipolar",
            "Psiquiatra",
            ["mudanças de humor", "comportamento impulsivo", "depressão"],
            False,
            "Grave",
        ),
        Doenca(
            "Esquizofrenia",
            "Psiquiatra",
            ["alucinações", "delírios", "isolamento social"],
            False,
            "Muito Grave",
        ),
        Doenca(
            "Transtorno de Estresse Pós-Traumático (TEPT)",
            "Psiquiatra",
            ["flashbacks", "ansiedade", "insônia"],
            False,
            "Moderada",
        ),
        Doenca(
            "Diabetes Tipo 1",
            "Endocrinologista",
            ["sede excessiva", "perda de peso", "fadiga"],
            False,
            "Grave",
        ),
        Doenca(
            "Diabetes Tipo 2",
            "Endocrinologista",
            ["sede excessiva", "fadiga", "visão embaçada"],
            False,
            "Moderada",
        ),
        Doenca(
            "Hipotireoidismo",
            "Endocrinologista",
            ["fadiga", "aumento de peso", "sensibilidade ao frio"],
            False,
            "Moderada",
        ),
        Doenca(
            "Hipertireoidismo",
            "Endocrinologista",
            ["perda de peso", "ansiedade", "insônia"],
            False,
            "Moderada",
        ),
        Doenca(
            "Síndrome de Cushing",
            "Endocrinologista",
            ["ganho de peso", "rosto arredondado", "fraqueza muscular"],
            True,
            "Grave",
        ),
    ]
    session.add_all(doencas)
    session.commit()

    # Dicionário de especialidades
    especialidades = {
        "Pediatria": Especialidade("Pediatria"),
        "Cardiologia": Especialidade("Cardiologia"),
        "Ortopedia": Especialidade("Ortopedia"),
        "Ginecologia": Especialidade("Ginecologia"),
        "Dermatologia": Especialidade("Dermatologia"),
        "Oftalmologia": Especialidade("Oftalmologia"),
        "Neurologia": Especialidade("Neurologia"),
        "Gastroenterologia": Especialidade("Gastroenterologia"),
        "Psiquiatria": Especialidade("Psiquiatria"),
        "Endocrinologia": Especialidade("Endocrinologia"),
    }

    # Adicionando as doenças às especialidades correspondentes
    for doenca in doencas:
        especialidade_nome = doenca.especialista
        if especialidade_nome in especialidades:
            especialidades[especialidade_nome].adicionar_doenca(doenca)

    # Exemplo de acesso aos sintomas em formato de lista:
    sintomas_lista = json.loads(doenca.sintomas)


# População de bairros
def populate_bairros(session):
    """Popula bairros no banco de dados."""
    bairros = [
        Bairro(
            nome="Santa Tereza",
            pop_total=22808,
            infra_saude="1 centro de saúde, 1 UPA, 2 clínicas particulares",
        ),
        Bairro(
            nome="Horto",
            pop_total=4360,
            infra_saude="1 centro de saúde, 1 UPA, 2 clínicas particulares",
        ),
        Bairro(
            nome="Sagrada familia",
            pop_total=34395,
            infra_saude="1 centro de saúde, 1 UPA, 2 clínicas particulares",
        ),
        Bairro(
            nome="Horto Florestal",
            pop_total=7920,
            infra_saude="1 centro de saúde, 1 UPA, 2 clínicas particulares",
        ),
        Bairro(
            nome="Colegio Batista",
            pop_total=3212,
            infra_saude="1 centro de saúde, 1 UPA, 2 clínicas particulares",
        ),
        Bairro(
            nome="Floresta",
            pop_total=5326,
            infra_saude="1 centro de saúde, 1 UPA, 2 clínicas particulares",
        ),
        Bairro(
            nome="Esplanada",
            pop_total=10012,
            infra_saude="1 centro de saúde, 1 UPA, 2 clínicas particulares",
        ),
        Bairro(
            nome="Pompeia",
            pop_total=9876,
            infra_saude="1 centro de saúde, 1 UPA, 2 clínicas particulares",
        ),
    ]
    session.add_all(bairros)
    session.commit()


# População de pacientes
def populate_pacientes(session):
    """Popula pacientes no banco de dados com distribuição por bairro e uma chance de 4% para pacientes de outros bairros."""
    bairros = session.query(Bairro).all()

    for bairro in bairros:
        for _ in range(bairro.pop_total):
            # 0.4% de chance para o paciente vir de outro bairro
            bairro_origem = (
                bairro if random.random() > 0.004 else random.choice(bairros)
            )
            paciente = Paciente(
                nome=fake.name(),
                idade=fake.random_int(min=1, max=100),
                sexo=fake.random_element(elements=("M", "F")),
                endereco=fake.address(),
                telefone=fake.phone_number(),
                id_bairro=bairro_origem.id,
            )
            session.add(paciente)

    session.commit()


# População de clínicas
def populate_clinicas(session):
    """Popula clínicas no banco de dados."""
    clinicas = [
        Clinica(
            nome="UPA Santa Tereza",
            tipo="Pública",
            capacidade_diaria=300,
            capacidade_leito=50,
            endereco="Rua A, 111",
        ),
        Clinica(
            nome="Centro de Saúde Horto",
            tipo="Pública",
            capacidade_diaria=200,
            capacidade_leito=20,
            endereco="Rua B, 222",
        ),
        Clinica(
            nome="Clínica Particular 1",
            tipo="Privada",
            capacidade_diaria=50,
            capacidade_leito=0,
            endereco="Rua C, 333",
        ),
        Clinica(
            nome="Clínica Particular 2",
            tipo="Privada",
            capacidade_diaria=30,
            capacidade_leito=0,
            endereco="Av. D, 444",
        ),
    ]
    session.add_all(clinicas)
    session.commit()


# Função para adicionar médicos a uma clínica
def add_medicos(clinica, medicos, qtd_clinicos, qtd_especialistas, especialidades):
    """Adiciona médicos para uma clínica específica com base na quantidade de clínicos gerais e especialistas."""
    # Adiciona clínicos gerais
    for _ in range(qtd_clinicos):
        medico = Medico(
            nome=fake.name(),
            especialidade="Clínico Geral",
            crm=fake.numerify(text="####/##"),
            id_clinica=clinica.id,
        )
        medicos.append(medico)

    # Adiciona especialistas
    for _ in range(qtd_especialistas):
        especialidade = random.choice(especialidades)
        medico = Medico(
            nome=fake.name(),
            especialidade=especialidade,
            crm=fake.numerify(text="####/##"),
            id_clinica=clinica.id,
        )
        medicos.append(medico)


def populate_medicos(session):
    """Popula médicos no banco de dados para clínicas públicas e privadas."""
    medicos = []
    clinicas = session.query(Clinica).all()

    # Define especialidades para clínicas públicas e privadas
    especialidades_publico = [
        "Pediatria",
        "Cardiologia",
        "Ortopedia",
        "Ginecologia",
        "Dermatologia",
    ]
    especialidades_privado = [
        "Oftalmologia",
        "Neurologia",
        "Gastroenterologia",
        "Psiquiatria",
        "Endocrinologia",
    ]

    for clinica in clinicas:
        if clinica.tipo == "Pública":
            if "UPA" in clinica.nome:
                # UPA: 10 clínicos gerais e 5 especialistas
                add_medicos(
                    clinica,
                    medicos,
                    qtd_clinicos=6,
                    qtd_especialistas=2,
                    especialidades=especialidades_publico,
                )
            elif "Centro de Saúde" in clinica.nome:
                # Centro de Saúde: 4 clínicos gerais e 1 pediatra
                add_medicos(
                    clinica,
                    medicos,
                    qtd_clinicos=4,
                    qtd_especialistas=1,
                    especialidades=["Pediatria"],
                )
        else:
            # Clínicas privadas: 5 especialistas, selecionados aleatoriamente entre as especialidades privadas
            add_medicos(
                clinica,
                medicos,
                qtd_clinicos=0,
                qtd_especialistas=5,
                especialidades=especialidades_privado,
            )

    # Salva todos os médicos gerados na sessão do banco de dados
    session.add_all(medicos)
    session.commit()


# População de agendamentos
def populate_agendamentos(session, pacientes, medicos, num_agendamentos=5):
    """Popula a tabela de agendamentos com múltiplos agendamentos para cada paciente."""
    agendamentos = []
    for paciente in pacientes:
        for _ in range(num_agendamentos):
            medico = random.choice(medicos)
            data_hora = fake.date_time_this_year() + timedelta(
                days=random.randint(1, 30)
            )
            agendamento = Agendamento(
                paciente_id=paciente.id,
                medico_id=medico.id,
                data_hora=data_hora,
                status_conclusao=random.choice(["agendado", "cancelado", "finalizado"]),
            )
            agendamentos.append(agendamento)
    session.add_all(agendamentos)
    session.commit()
    logging.info(f"Total de Agendamentos: {session.query(Agendamento).count()}")


# População de profissionais de saúde
def populate_profissionais_saude(session):
    """Popula profissionais de saúde (enfermeiros e técnicos de enfermagem)."""
    profissionais = [
        ProfissionalSaude(
            nome=fake.name(),
            tipo=random.choice(["Enfermeiro", "Técnico de Enfermagem"]),
        )
        for _ in range(25)  # 15 enfermeiros e 10 técnicos
    ]
    session.add_all(profissionais)
    session.commit()


# População de atendimentos pulados
def populate_atendimento_pulado(session):
    """Popula a tabela atendimentos_pulados com registros de agendamentos não concluídos."""
    atendimentos_pulados = []
    agendamentos = (
        session.query(Agendamento)
        .filter(Agendamento.status_conclusao == "cancelado")
        .all()
    )

    for agendamento in agendamentos:
        atendimento_pulado = AtendimentoPulado(
            id_paciente=agendamento.paciente_id,
            id_bairro=random.choice(session.query(Bairro).all()).id,
            id_doenca=random.choice(session.query(Doenca).all()).id,
            motivo="Agendamento cancelado",
            data_tentativa=agendamento.data_hora,
        )
        atendimentos_pulados.append(atendimento_pulado)

    session.add_all(atendimentos_pulados)
    session.commit()
    logging.info(
        f"Total de Atendimentos Pulados: {session.query(AtendimentoPulado).count()}"
    )


# População de atendimentos profissionais
def populate_atendimento_profissional(session):
    """Popula a tabela de atendimento_profissional com dados baseados em agendamentos."""
    atendimentos_profissionais = []
    agendamentos = session.query(Agendamento).all()

    for agendamento in agendamentos:
        if (
            agendamento.status_conclusao == "finalizado"
        ):  # Apenas para agendamentos finalizados
            status_opcoes = ["concluído", "em andamento", "cancelado"]
            conclusao = fake.sentence()

            # Lógica adicional para status de conclusão mais realista
            if random.random() < 0.1:  # Probabilidade de 10% de óbito
                status = "óbito"
                conclusao += " Paciente faleceu durante o atendimento."
            else:
                status = random.choice(status_opcoes)
                if status == "concluído":
                    conclusao += " Atendimento foi finalizado com sucesso."
                elif status == "em andamento":
                    conclusao += " Atendimento ainda em andamento."

            atendimento = AtendimentoProfissional(
                id_atendimento=agendamento.id,  # Corrigido para usar id_atendimento
                id_profissional=random.choice(
                    session.query(ProfissionalSaude).all()
                ).id,
                funcao="Consulta",
            )
            atendimentos_profissionais.append(atendimento)

    session.add_all(atendimentos_profissionais)
    session.commit()
    logging.info(
        f"Total de Atendimentos Profissionais: {session.query(AtendimentoProfissional).count()}"
    )


# Função principal de população
def populate_database(session):
    """Popula o banco de dados inteiro."""
    reset_database(session)
    populate_bairros(session)
    populate_pacientes(session)
    populate_clinicas(session)
    populate_medicos(session)
    populate_doencas(session)

    # Obter dados de pacientes e médicos após criação
    pacientes = session.query(Paciente).all()
    medicos = session.query(Medico).all()
    populate_agendamentos(session, pacientes, medicos)
    populate_profissionais_saude(session)
    populate_atendimento_profissional(session)
    populate_atendimento_pulado(session)

    logging.info("Banco de dados populado com sucesso!")
