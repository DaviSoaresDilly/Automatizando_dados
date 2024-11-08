from sqlalchemy import and_
import pandas as pd
from application.models import Paciente, Atendimento, Doenca, Bairro, Medico
from application.reports.date_utils import calculate_date_range

# Funções utilitárias
def execute_query_to_df(query, session):
    """Executa a consulta e converte o resultado para DataFrame, com tratamento de erros."""
    try:
        return pd.read_sql(query.statement, session.bind)
    except Exception as e:
        print(f"Erro ao executar a consulta: {e}")
        return pd.DataFrame()  # Retorna DataFrame vazio em caso de erro

# Funções de busca de dados
def get_doenca_list(session):
    """Retorna uma lista de todas as doenças registradas."""
    return [d.nome for d in session.query(Doenca).distinct()]

def get_especialidades_list(session):
    """Retorna uma lista de todas as especialidades registradas."""
    return [d.especialista for d in session.query(Doenca.especialista).distinct()]

def get_doencas_por_especialidade(session, especialidade):
    """Retorna lista de doenças conforme a especialidade selecionada."""
    query = session.query(Doenca.nome).distinct()
    if especialidade != "Todas":
        query = query.filter(Doenca.especialista == especialidade)
    return [d.nome for d in query]

def get_bairros_list(session):
    """Retorna uma lista de todos os bairros registrados."""
    return [b.nome for b in session.query(Bairro).distinct()]

def fetch_data(session, period, ano, mes, trimestre, doenca, genero, faixa_etaria):
    """Consulta dados de pacientes com filtros e cria uma coluna de faixa etária."""
    data_inicio, data_fim = calculate_date_range(period, ano, mes, trimestre)
    print(f"Período: {period}, Data de início: {data_inicio}, Data de fim: {data_fim}")

    # Construção da consulta
    query = (
        session.query(Paciente.idade.label("Idade"), Paciente.sexo.label("Sexo"), Doenca.nome.label("Doenca"))
        .join(Atendimento, Paciente.id == Atendimento.id_paciente)
        .join(Doenca, Atendimento.id_doenca == Doenca.id)
        .filter(and_(Atendimento.data_atendimento >= data_inicio, Atendimento.data_atendimento <= data_fim))
    )

    # Aplicação dos filtros adicionais
    if doenca != "Todas":
        query = query.filter(Doenca.nome == doenca)
    if genero != "Todos":
        query = query.filter(Paciente.sexo == genero)

    # Executa a consulta e converte o resultado em DataFrame
    df = pd.DataFrame([{"Idade": idade, "Sexo": sexo, "Doenca": doenca} for idade, sexo, doenca in query.all()])

    # Verificação de presença da coluna "Idade"
    if "Idade" not in df.columns:
        print("Erro: Coluna 'Idade' não encontrada.")
        return pd.DataFrame()

    # Adiciona a coluna "Faixa Etária"
    df["Faixa Etária"] = pd.cut(df["Idade"], bins=[0, 12, 18, 40, 60, 100], labels=["Criança", "Adolescente", "Adulto", "Meia-Idade", "Idoso"])

    # Aplica o filtro de faixa etária
    if faixa_etaria != "Todas":
        df = df[df["Faixa Etária"] == faixa_etaria]

    return df

def fetch_data_bairros(session, period, ano, mes, trimestre, doencas, bairro):
    """Consulta dados por bairro com filtros de período e doença."""
    data_inicio, data_fim = calculate_date_range(period, ano, mes, trimestre)
    print(f"Período: {period}, Data de início: {data_inicio}, Data de fim: {data_fim}")

    # Construção da consulta
    query = (
        session.query(Bairro.nome.label("Bairro"), Doenca.nome.label("Doenca"))
        .select_from(Atendimento)
        .join(Paciente, Paciente.id == Atendimento.id_paciente)
        .join(Doenca, Atendimento.id_doenca == Doenca.id)
        .join(Bairro, Atendimento.id_bairro == Bairro.id)
        .filter(and_(Atendimento.data_atendimento >= data_inicio, Atendimento.data_atendimento <= data_fim))
    )

    # Aplicação dos filtros adicionais
    if doencas != ["Todas"]:
        query = query.filter(Doenca.nome.in_(doencas))
    if bairro != "Todos":
        query = query.filter(Bairro.nome == bairro)

    # Executa a consulta e converte o resultado em DataFrame
    bairro = query.all()
    df = pd.DataFrame([(b.Bairro, b.Doenca) for b in bairro], columns=["Bairro", "Doenca"])

    # Log para verificar o DataFrame resultante
    print(f"DataFrame resultante: {df.head()}")

    return df

def fetch_data_atendimentos(session, period, ano, mes, trimestre, medico):
    """Consulta dados de atendimentos com filtros de período e médico."""
    data_inicio, data_fim = calculate_date_range(period, ano, mes, trimestre)
    print(f"Período: {period}, Data de início: {data_inicio}, Data de fim: {data_fim}")

    # Construção da consulta
    query = (
        session.query(
            Atendimento.data_atendimento.label("Data_Atendimento"),
            Medico.nome.label("Medico"),
            Paciente.idade.label("Idade"),
            Paciente.sexo.label("Sexo")
        )
        .join(Medico, Atendimento.id_medico == Medico.id)
        .join(Paciente, Atendimento.id_paciente == Paciente.id)
        .filter(and_(Atendimento.data_atendimento >= data_inicio, Atendimento.data_atendimento <= data_fim))
    )

    # Aplicação dos filtros adicionais
    if medico != "Todos":
        query = query.filter(Medico.nome == medico)

    # Executa a consulta e converte o resultado em DataFrame manualmente
    atendimentos = query.all()
    df = pd.DataFrame([(a.Data_Atendimento, a.Medico, a.Idade, a.Sexo) for a in atendimentos],
                      columns=["Data_Atendimento", "Medico", "Idade", "Sexo"])

    return df
