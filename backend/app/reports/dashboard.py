# backend/app/reports/dashboard.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))

import streamlit as st
import pandas as pd
from sqlalchemy.orm import Session
from app.database import get_session, create_app
from app.reports.generate_reports import (
    generate_occupacao_report,
    generate_age_gender_distribution_report,
    generate_doenca_por_bairro_report
)
from app.reports.visualize import (
    plot_ocupacao_historico_previsao,
    plot_distribution_by_age_gender,
    plot_doenca_por_bairro
)

# Inicializa o app Flask e a sessão do banco de dados
app = create_app()
session: Session = get_session()

# Configurações do Streamlit
st.set_page_config(page_title="Dashboard de Análise Hospitalar", layout="wide")

# Título do Dashboard
st.title("Dashboard de Análise Hospitalar")

# Seção de Ocupação de Leitos
st.header("Análise de Ocupação de Leitos")
clinica_id = st.sidebar.number_input("ID da Clínica", min_value=1, value=1, step=1)
dias_previstos = st.sidebar.slider("Dias para previsão", 1, 90, 30)

# Gera e exibe o relatório de ocupação
try:
    df_occupacao = generate_occupacao_report(session, clinica_id, dias_previstos)
    st.write("Relatório de Ocupação de Leitos")
    st.dataframe(df_occupacao)
    plot_ocupacao_historico_previsao(df_occupacao, df_occupacao, "Clínica Exemplo")
except Exception as e:
    st.error(f"Erro ao gerar o relatório de ocupação: {e}")

# Seção de Distribuição por Idade e Gênero
st.header("Distribuição de Doenças por Idade e Gênero")
try:
    df_age_gender = generate_age_gender_distribution_report(session)
    st.write("Distribuição de Doenças por Idade e Gênero")
    st.dataframe(df_age_gender)
    plot_distribution_by_age_gender(df_age_gender)
except Exception as e:
    st.error(f"Erro ao gerar o relatório de distribuição por idade e gênero: {e}")

# Seção de Doenças por Bairro
st.header("Distribuição de Doenças por Bairro")
try:
    df_doenca_bairro = generate_doenca_por_bairro_report(session)
    st.write("Distribuição de Doenças por Bairro")
    st.dataframe(df_doenca_bairro)
    plot_doenca_por_bairro(df_doenca_bairro)
except Exception as e:
    st.error(f"Erro ao gerar o relatório de doenças por bairro: {e}")