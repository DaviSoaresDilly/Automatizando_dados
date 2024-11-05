# application/reports/dashboard.py

import sys
import os
from sqlalchemy import and_
import streamlit as st
import pandas as pd
from datetime import date, datetime, timedelta
from sqlalchemy.orm import Session
import matplotlib.pyplot as plt
import seaborn as sns

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from application.models import Paciente, Atendimento, Doenca
from application.database import get_session, create_app

# Inicializa o app Flask
app = create_app()

# Configurações do Streamlit
st.set_page_config(page_title="Distribuição de Doenças por Idade e Gênero", layout="wide")
st.title("Análise de Distribuição de Doenças por Idade e Gênero")

# Proposta da Análise
st.markdown("""
Esta análise visa fornecer uma visão detalhada da distribuição de doenças por faixa etária e gênero em diferentes períodos (mensal, trimestral e anual). Isso ajuda a identificar padrões e tendências na incidência de doenças, permitindo uma melhor alocação de recursos e planejamento estratégico.
""")

# Função para buscar os nomes das doenças dinamicamente com a sessão ativa
def get_doenca_list(session):
    return [d.nome for d in session.query(Doenca).distinct()]

# Carregar dados para o filtro de doenças
with app.app_context():
    session = get_session()
    # Popula a lista de doenças
    doencas = ["Todas"] + get_doenca_list(session)
    session.close()

# Menu de Filtros
st.sidebar.header("Filtros")
selected_period = st.sidebar.selectbox("Período", ["Mensal", "Trimestral", "Anual"], index=2)
selected_ano = st.sidebar.selectbox("Ano", list(range(2022, 2025)), index=2)
selected_mes = st.sidebar.selectbox("Mês", list(range(1, 13)), format_func=lambda x: datetime(2022, x, 1).strftime('%B')) if selected_period == "Mensal" else None
selected_trimestre = st.sidebar.selectbox("Trimestre", ["1º Trimestre", "2º Trimestre", "3º Trimestre", "4º Trimestre"]) if selected_period == "Trimestral" else None
selected_doenca = st.sidebar.selectbox("Doença", doencas)
selected_genero = st.sidebar.selectbox("Gênero", ["Todos", "M", "F"])
selected_faixa_etaria = st.sidebar.selectbox("Faixa Etária", ["Todas", "Criança", "Adolescente", "Adulto", "Meia-Idade", "Idoso"])

# Função para buscar dados da distribuição de doenças com base nos filtros de idade e gênero
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

def calculate_date_range(period: str, ano: int, mes: int = None, trimestre: str = None):
    """
    Calcula a data de início com base no período selecionado.
    """
    if period == "Mensal" and mes:
        start_date = date(ano, mes, 1)
        end_date = (datetime(ano, mes, 1) + pd.DateOffset(months=1) - pd.DateOffset(days=1)).date()
    elif period == "Trimestral" and trimestre:
        if trimestre == "1º Trimestre":
            start_date = date(ano, 1, 1)
        elif trimestre == "2º Trimestre":
            start_date = date(ano, 4, 1)
        elif trimestre == "3º Trimestre":
            start_date = date(ano, 7, 1)
        elif trimestre == "4º Trimestre":
            start_date = date(ano, 10, 1)
        end_date = (datetime(ano, start_date.month, 1) + pd.DateOffset(months=3) - pd.DateOffset(days=1)).date()
    elif period == "Anual":
        start_date = date(ano, 1, 1)
        end_date = date(ano, 12, 31)
    else:
        raise ValueError("Período inválido")
    
    # Log para verificar a data de início calculada
    print(f"Data de início calculada para o período '{period}': {start_date}")
    return start_date, end_date

def get_period_label(period, start_date, end_date):
    if period == "Mensal":
        return start_date.strftime("%B de %Y")
    elif period == "Trimestral":
        return f"{start_date.strftime('%B')} a {end_date.strftime('%B de %Y')}"
    elif period == "Anual":
        return start_date.strftime("%Y")
    return ""

# Busca os dados com base nos filtros selecionados
with app.app_context():
    session = get_session()
    data_inicio, data_fim = calculate_date_range(selected_period, selected_ano, selected_mes, selected_trimestre)
    df = fetch_data(session, selected_period, selected_ano, selected_mes, selected_trimestre, selected_doenca, selected_genero, selected_faixa_etaria)
    session.close()

# Verifica se o DataFrame não está vazio
if not df.empty:
    # Criação do layout de grade
    col1, col2 = st.columns(2)

    with col1:
        # Exibição da tabela de dados
        st.subheader("Tabela de Dados")
        st.dataframe(df.style.set_properties(**{'font-size': '20pt'}))

    with col2:
        # Criação do Heatmap
        period_label = get_period_label(selected_period, data_inicio, data_fim)
        st.subheader(f"Distribuição de Doenças - {period_label}")

        # Criação de uma tabela de contagem para o heatmap
        df_pivot = pd.pivot_table(
            df,
            values="Doenca",
            index="Faixa Etária",
            columns="Sexo",
            aggfunc="count",
            fill_value=0,
            observed=False  # Adiciona o parâmetro observed=False
        )

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(df_pivot, annot=True, fmt="d", cmap="coolwarm", cbar=True, ax=ax, annot_kws={"size": 20})
        ax.set_title(f"Distribuição de Doenças por Faixa Etária e Gênero ({period_label})", fontsize=20)
        ax.set_xlabel("Sexo", fontsize=20)
        ax.set_ylabel("Faixa Etária", fontsize=20)
        ax.tick_params(axis='both', which='major', labelsize=20)
        st.pyplot(fig)
else:
    st.warning("Nenhum dado disponível para os filtros selecionados.")
