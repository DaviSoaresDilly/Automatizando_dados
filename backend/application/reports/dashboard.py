# app/reports/dashboard.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import streamlit as st
import pandas as pd

from matplotlib import pyplot as plt
from sqlalchemy.orm import Session
from application.database import get_session, create_app
from application.reports.generate_reports import (
    generate_occupacao_report,
    generate_age_gender_distribution_report,
    generate_doenca_por_bairro_report
)
from application.reports.visualize import (
    plot_ocupacao_historico_previsao,
    plot_distribution_by_age_gender,
    plot_doenca_por_bairro
)

# Inicializa o app Flask
app = create_app()

# Configurações do Streamlit
st.set_page_config(page_title="Dashboard de Análise Hospitalar", layout="wide")

# Título do Dashboard
st.title("Dashboard de Análise Hospitalar")

# Configura sidebar
clinica_id = st.sidebar.number_input("ID da Clínica", min_value=1, value=1, step=1)
dias_previstos = st.sidebar.slider("Dias para previsão", 1, 90, 30)

# Envolva as operações no contexto da aplicação Flask
with app.app_context():
    session: Session = get_session()

    # Seção de Ocupação de Leitos
    st.header("Análise de Ocupação de Leitos")
    st.write("Esta seção fornece uma visão geral da ocupação de leitos nos últimos seis meses, "
             "incluindo uma previsão de ocupação para os próximos dias selecionados.")
    
    try:
        df_occupacao = generate_occupacao_report(session, clinica_id, dias_previstos)
        
        # Verificação e ajuste de colunas no DataFrame
        if 'Ocupação Histórica' in df_occupacao.columns and 'Ocupação Prevista' in df_occupacao.columns:
            st.write("Relatório de Ocupação de Leitos")
            st.dataframe(df_occupacao)
            
            # Exibe o gráfico de ocupação de leitos com `fig`
            fig, ax = plt.subplots()
            plot_ocupacao_historico_previsao(
                df_occupacao[['data', 'Ocupação Histórica']],
                df_occupacao[['data', 'Ocupação Prevista']],
                f"Clínica {clinica_id}",
                fig, ax  # Passa a figura e o eixo para configuração
            )
            st.pyplot(fig)
        else:
            st.error("Erro ao processar os dados de ocupação.")
    except Exception as e:
        st.error(f"Erro ao gerar o relatório de ocupação: {e}")

    # Seção de Distribuição de Doenças por Faixa Etária e Sexo
    st.header("Distribuição de Doenças por Idade e Gênero")
    st.write("Esta análise mostra a distribuição de doenças por faixa etária e gênero, permitindo identificar "
             "quais doenças prevalecem em diferentes grupos.")
    
    try:
        df_distribuicao = generate_age_gender_distribution_report(session)
        st.write("Distribuição de Doenças")
        st.dataframe(df_distribuicao)
        
        # Exibe o gráfico de distribuição de doenças com `fig`
        fig, ax = plt.subplots()
        plot_distribution_by_age_gender(df_distribuicao, fig, ax)
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Erro ao gerar o relatório de distribuição por idade e gênero: {e}")

    # Seção de Quantidade de Doenças por Bairro
    st.header("Distribuição de Doenças por Bairro")
    st.write("Este gráfico detalha a quantidade de casos de doenças por bairro, fornecendo insights sobre as áreas "
             "mais afetadas e a prevalência de doenças específicas.")
    
    try:
        df_doenca_bairro = generate_doenca_por_bairro_report(session)
        st.write("Distribuição de Doenças por Bairro")
        st.dataframe(df_doenca_bairro)
        
        # Exibe o gráfico de doenças por bairro com `fig`
        fig, ax = plt.subplots()
        plot_doenca_por_bairro(df_doenca_bairro, fig, ax)
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Erro ao gerar o relatório de doenças por bairro: {e}")

    # Fecha a sessão do banco
    session.close()
    