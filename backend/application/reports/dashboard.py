# application/reports/dashboard.py

import sys
import os
import streamlit as st
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from application.models import Bairro, Clinica, Doenca
from matplotlib import pyplot as plt
from sqlalchemy.orm import Session
from application.database import get_session, create_app
from application.reports.generate_reports import (
    generate_filtered_occupacao_report,
    generate_filtered_age_gender_distribution_report,
    generate_filtered_doenca_por_bairro_report,
)

from application.reports.visualize import (
    plot_ocupacao_historico_previsao,
    plot_distribution_by_age_gender,
    plot_doenca_por_bairro,
)

# Inicializa o app Flask
app = create_app()

# Configurações do Streamlit
st.set_page_config(page_title="Dashboard de Análise Hospitalar", layout="wide")
st.title("Dashboard de Análise Hospitalar")

# Definir os filtros específicos para cada análise
with app.app_context():
    session = get_session()
    
    # Carregar dados dos filtros
    clinicas = [c[0] for c in session.query(Clinica.nome).distinct().all()]
    bairros = [b[0] for b in session.query(Bairro.nome).distinct().all()]
    doencas = [d[0] for d in session.query(Doenca.nome).distinct().all()]

# Filtros - Ocupação de Leitos
st.sidebar.header("Filtros - Ocupação de Leitos")
selected_clinica = st.sidebar.selectbox("Clínica", clinicas, key="clinica_selectbox")
ocupacao_period = st.sidebar.selectbox("Período de Ocupação", ["Mensal", "Trimestral", "Anual"], key="ocupacao_period_selectbox")

# Filtros - Distribuição por Idade e Gênero
st.sidebar.header("Filtros - Distribuição por Idade e Gênero")
selected_genero = st.sidebar.selectbox("Gênero", ["Masculino", "Feminino", "Outro", "Todos"], key="genero_selectbox")
selected_faixa_etaria = st.sidebar.selectbox("Faixa Etária", ["Criança", "Adolescente", "Adulto", "Meia-Idade", "Idoso"], key="faixa_etaria_selectbox")
idade_period = st.sidebar.selectbox("Período", ["Mensal", "Trimestral", "Anual"], key="idade_period_selectbox")

# Filtros - Distribuição por Bairro
st.sidebar.header("Filtros - Distribuição por Bairro")
selected_doenca_bairro = st.sidebar.selectbox("Doença", ["Todas"] + doencas, key="doenca_bairro_selectbox")
selected_bairro = st.sidebar.selectbox("Bairro", ["Todos"] + bairros, key="bairro_selectbox")
bairro_period = st.sidebar.selectbox("Período", ["Mensal", "Trimestral", "Anual"], key="bairro_period_selectbox")


with app.app_context():
    session = get_session()

    # --- Ocupação de Leitos ---
    st.header("Análise de Ocupação de Leitos")
    try:
        df_occupacao = generate_filtered_occupacao_report(session, selected_clinica, ocupacao_period)
        if not df_occupacao.empty:
            st.dataframe(df_occupacao)

            fig, ax = plt.subplots()
            plot_ocupacao_historico_previsao(
                df_occupacao[["data", "Ocupação Histórica"]],
                df_occupacao[["data", "Ocupação Prevista"]],
                f"Ocupação de Leitos - {selected_clinica}",
                fig,
                ax
            )
            st.pyplot(fig)
        else:
            st.warning("Nenhum dado disponível para o filtro selecionado.")
    except Exception as e:
        st.error(f"Erro ao gerar o relatório de ocupação: {e}")

    # --- Distribuição por Idade e Gênero ---
    st.header("Distribuição de Doenças por Idade e Gênero")
    try:
        df_distribuicao = generate_filtered_age_gender_distribution_report(
            session, selected_genero, selected_faixa_etaria, idade_period
        )
        if not df_distribuicao.empty:
            st.dataframe(df_distribuicao)

            fig, ax = plt.subplots()
            plot_distribution_by_age_gender(df_distribuicao, fig, ax)
            st.pyplot(fig)
        else:
            st.warning("Nenhum dado disponível para o filtro selecionado.")
    except Exception as e:
        st.error(f"Erro ao gerar o relatório de distribuição por idade e gênero: {e}")

    # --- Distribuição por Bairro ---
    st.header("Distribuição de Doenças por Bairro")
    try:
        df_doenca_bairro = generate_filtered_doenca_por_bairro_report(
            session, selected_doenca_bairro, selected_bairro, bairro_period
        )
        if not df_doenca_bairro.empty:
            st.dataframe(df_doenca_bairro)

            fig, ax = plt.subplots()
            plot_doenca_por_bairro(df_doenca_bairro, fig, ax)
            st.pyplot(fig)
        else:
            st.warning("Nenhum dado disponível para o filtro selecionado.")
    except Exception as e:
        st.error(f"Erro ao gerar o relatório de doenças por bairro: {e}")

    session.close()