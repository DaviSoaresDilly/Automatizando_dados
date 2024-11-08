# application/reports/statistical_analysis.py

from datetime import datetime
import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
from application.database import get_session
from application.models import Medico
from data_fetcher import get_especialidades_list, fetch_data_atendimentos
from date_utils import calculate_date_range, get_period_label
from report_generator import generate_report

# Função para realizar a análise estatística de atendimentos e médicos
def analise_estatistica_atendimentos_medicos(app):
    st.header("Análise Estatística de Atendimentos e Médicos")

    # Proposta da Análise
    st.markdown("""
    ### Proposta da Análise

    A análise estatística de atendimentos e médicos se concentra em entender a distribuição e características dos atendimentos realizados pelos médicos. No contexto da saúde pública, essa análise pode ser usada para identificar padrões de atendimento, carga de trabalho dos médicos e eficiência dos serviços de saúde. Esta análise ajuda a identificar áreas de melhoria e otimização dos recursos de saúde.

    **Benefícios da Análise**:
    - **Identificação de Padrões de Atendimento**: A análise permite identificar padrões nos atendimentos realizados pelos médicos.
    - **Planejamento de Recursos**: Compreender a distribuição dos atendimentos ajuda na alocação eficiente de recursos, como médicos e equipamentos.
    - **Otimização dos Serviços de Saúde**: Identificar áreas de melhoria pode ajudar na implementação de medidas para otimizar os serviços de saúde.
    - **Tomada de Decisões Informadas**: Fornece uma base sólida de dados para apoiar decisões estratégicas em saúde pública.
    """)

    # Carregar dados para o filtro de médicos e períodos
    with app.app_context():
        session = get_session()
        # Popula a lista de médicos
        medicos = ["Todos"] + [m.nome for m in session.query(Medico).distinct()]
        session.close()

    # Menu de Filtros
    st.sidebar.header("Filtros - Atendimentos e Médicos")
    selected_period = st.sidebar.selectbox("Período", ["Mensal", "Trimestral", "Anual"], index=2, key="periodo_atendimentos")
    selected_ano = st.sidebar.selectbox("Ano", list(range(2022, 2025)), index=2, key="ano_atendimentos")
    selected_mes = st.sidebar.selectbox("Mês", list(range(1, 13)), format_func=lambda x: datetime(2022, x, 1).strftime('%B'), key="mes_atendimentos") if selected_period == "Mensal" else None
    selected_trimestre = st.sidebar.selectbox("Trimestre", ["1º Trimestre", "2º Trimestre", "3º Trimestre", "4º Trimestre"], key="trimestre_atendimentos") if selected_period == "Trimestral" else None
    selected_medico = st.sidebar.selectbox("Médico", medicos, key="medico_atendimentos")

    # Busca os dados com base nos filtros selecionados
    with app.app_context():
        session = get_session()
        df = fetch_data_atendimentos(session, selected_period, selected_ano, selected_mes, selected_trimestre, selected_medico)
        session.close()

    # Verifica se o DataFrame não está vazio
    if not df.empty:
        # Log para verificar o número de registros carregados
        print(f"Número de registros carregados: {len(df)}")

        period_label = get_period_label(selected_period, df['Data_Atendimento'].min(), df['Data_Atendimento'].max())

        with st.container():
            # Criação do layout de grade
            col1, col2 = st.columns([0.4, 0.6])

            with col1:
                # Exibição da tabela de dados
                st.markdown(f"<h3 style='text-align: center;'>Tabela de Dados - {selected_ano}</h3>", unsafe_allow_html=True)
                st.dataframe(df)

            with col2:
                # Gráfico de Distribuição de Idade dos Pacientes
                st.markdown(f"<h3 style='text-align: center;'>Distribuição de Idade dos Pacientes - {period_label}</h3>", unsafe_allow_html=True)
                fig, ax = plt.subplots(figsize=(10, 6))
                sns.histplot(df["Idade"], bins=20, kde=True, ax=ax, color="#3A84DF")
                ax.set_xlabel("Idade", fontsize=12)
                ax.set_ylabel("Frequência", fontsize=12)
                ax.set_title("Distribuição de Idade dos Pacientes", fontsize=16)
                for p in ax.patches:
                    ax.annotate(f'{int(p.get_height())}', 
                                (p.get_x() + p.get_width() / 2, p.get_height()), 
                                ha='center', va='bottom', fontsize=10, color="black")
                st.pyplot(fig)
                st.markdown("<p style='text-align: center;'>Gráfico mostrando a distribuição de idade dos pacientes atendidos durante o período selecionado.</p>", unsafe_allow_html=True)

        with st.container():
            # Margem para o próximo gráfico
            st.markdown("<br><br>", unsafe_allow_html=True)

            # Gráfico de Distribuição de Atendimentos por Médico
            st.markdown(f"<h3 style='text-align: center;'>Distribuição de Atendimentos por Médico - {period_label}</h3>", unsafe_allow_html=True)
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.countplot(x="Medico", data=df, ax=ax, hue="Medico", palette="Set2", legend=False)
            ax.set_xlabel("Médico", fontsize=12)
            ax.set_ylabel("Número de Atendimentos", fontsize=12)
            ax.set_title("Distribuição de Atendimentos por Médico", fontsize=16)
            plt.xticks(rotation=45, ha='right')
            for p in ax.patches:
                ax.annotate(f'{int(p.get_height())}', 
                            (p.get_x() + p.get_width() / 2, p.get_height()), 
                            ha='center', va='bottom', fontsize=10, color="black")
            st.pyplot(fig)

        with st.container():
            st.markdown("<br><br><br>", unsafe_allow_html=True)

            # Gráfico de Barras Empilhadas para Distribuição de Atendimentos por Gênero
            st.markdown(f"<h3 style='text-align: center;'>Distribuição de Atendimentos por Gênero - {period_label}</h3>", unsafe_allow_html=True)
            fig, ax = plt.subplots(figsize=(10, 6))
            df_gender = df.groupby(['Sexo']).size().reset_index(name='Atendimentos')
            sns.barplot(x='Sexo', y='Atendimentos', data=df_gender, ax=ax, palette=['pink', 'blue'], legend=False)
            ax.set_xlabel("Gênero", fontsize=12)
            ax.set_ylabel("Número de Atendimentos", fontsize=12)
            ax.set_title("Distribuição de Atendimentos por Gênero", fontsize=16)
            for p in ax.patches:
                ax.annotate(f'{int(p.get_height())}', 
                            (p.get_x() + p.get_width() / 2, p.get_height()), 
                            ha='center', va='bottom', fontsize=10, color="black")
            st.pyplot(fig)

        # Gerar Relatório
        if st.button("Gerar Relatório", key="gerar_relatorio_atendimentos"):
            analysis_summary = (
                "Esta análise mostra a distribuição de atendimentos por médicos, idade dos pacientes e gênero. "
                "Observa-se que determinados médicos têm uma carga de trabalho maior, e que a distribuição de idade e gênero dos pacientes é variada."
            )
            output_path_pdf = f'relatorio_atendimentos_medicos_{selected_ano}.pdf'
            output_path_csv = f'tabela_atendimentos_medicos_{selected_ano}.csv'
            generate_report(df, analysis_summary, output_path_pdf, output_path_csv, selected_ano)
            st.success(f"Relatório gerado com sucesso: {os.path.join('reports', output_path_pdf)}")
            st.success(f"Tabela de dados gerada com sucesso: {os.path.join('reports', output_path_csv)}")
    else:
        st.warning("Nenhum dado disponível para os filtros selecionados.")
        st.stop()