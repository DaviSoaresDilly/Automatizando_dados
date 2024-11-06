# application/reports/data_fetcher.py

from sqlalchemy import and_
import pandas as pd
from application.models import Paciente, Atendimento, Doenca
from application.reports.date_utils import calculate_date_range

def get_doenca_list(session):
    return [d.nome for d in session.query(Doenca).distinct()]

def fetch_data(session, period, ano, mes, trimestre, doenca, genero, faixa_etaria):
    """Consulta dados de doenças com filtros e calcula a faixa etária."""
    data_inicio, data_fim = calculate_date_range(period, ano, mes, trimestre)

    # Log para verificar o período calculado
    print(f"Período selecionado: {period}")
    print(f"Data de início: {data_inicio}, Data de fim: {data_fim}")

    query = (
        session.query(Paciente.idade.label("Idade"), Paciente.sexo.label("Sexo"), Doenca.nome.label("Doenca"))
        .join(Atendimento, Paciente.id == Atendimento.id_paciente)
        .join(Doenca, Atendimento.id_doenca == Doenca.id)
        .filter(and_(Atendimento.data_atendimento >= data_inicio, Atendimento.data_atendimento <= data_fim))
    )

    if doenca != "Todas":
        query = query.filter(Doenca.nome == doenca)
    if genero != "Todos":
        query = query.filter(Paciente.sexo == genero)

    # Executa a consulta e converte para DataFrame
    dados = [{"Idade": idade, "Sexo": sexo, "Doenca": doenca} for idade, sexo, doenca in query.all()]
    df = pd.DataFrame(dados)

    # Verifica se a coluna 'Idade' está no DataFrame
    if "Idade" not in df.columns:
        print("Erro: Coluna 'Idade' não encontrada no DataFrame.")
        return pd.DataFrame()  # Retorna DataFrame vazio em caso de erro

    # Cria a coluna "Faixa Etária" com os intervalos definidos
    df["Faixa Etária"] = pd.cut(df["Idade"], bins=[0, 12, 18, 40, 60, 100], labels=["Criança", "Adolescente", "Adulto", "Meia-Idade", "Idoso"])

    # Aplica filtro de faixa etária, se definido
    if faixa_etaria != "Todas":
        df = df[df["Faixa Etária"] == faixa_etaria]

    return df