# application/reports/predictive_analysis.py

from datetime import date, timedelta
import pandas as pd
import numpy as np
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, DBSCAN
from sklearn.decomposition import PCA
from statsmodels.tsa.arima.model import ARIMA
from application.database import get_session
from application.models import Atendimento, Clinica, Paciente, Doenca
from analyze_occupacao_arima import prever_ocupacao_arima

def analise_ocupacao_leitos(app):
    st.header("Análise Preditiva de Ocupação de Leitos")

    # Proposta da Análise
    st.markdown("""
    ### Proposta da Análise

    A análise preditiva de ocupação de leitos utiliza dados históricos para prever a demanda futura de leitos hospitalares. No contexto da saúde pública, essa análise pode ser usada para antecipar picos de demanda e planejar a alocação de recursos de forma eficiente. Esta análise ajuda a identificar períodos de alta ocupação e a tomar decisões informadas para otimizar a gestão hospitalar.

    **Benefícios da Análise**:
    - **Antecipação de Picos de Demanda**: A análise permite prever períodos de alta ocupação de leitos.
    - **Planejamento de Recursos**: Compreender a demanda futura ajuda na alocação eficiente de recursos, como leitos e profissionais de saúde.
    - **Otimização da Gestão Hospitalar**: Identificar períodos de alta ocupação pode ajudar na implementação de medidas para otimizar a gestão hospitalar.
    - **Tomada de Decisões Informadas**: Fornece uma base sólida de dados para apoiar decisões estratégicas em saúde pública.
    """)

    # Carregar dados para o filtro de clínicas
    with app.app_context():
        session = get_session()
        clinicas = session.query(Clinica).all()
        session.close()

    # Menu de Filtros
    st.sidebar.header("Filtros - Ocupação de Leitos")
    selected_clinica = st.sidebar.selectbox("Clínica", [c.nome for c in clinicas], key="clinica_ocupacao")
    selected_mes = st.sidebar.selectbox("Mês", list(range(1, 13)), format_func=lambda x: date(2025, x, 1).strftime('%B'), key="mes_ocupacao")

    # Busca os dados com base nos filtros selecionados
    with app.app_context():
        session = get_session()
        clinica_id = next(c.id for c in clinicas if c.nome == selected_clinica)
        previsao_df = prever_ocupacao_arima(clinica_id)
        session.close()

    # Filtrar a previsão para o mês selecionado
    previsao_df['data'] = pd.to_datetime(previsao_df['data'])
    previsao_df = previsao_df[previsao_df['data'].dt.month == selected_mes]

    # Verifica se o DataFrame não está vazio
    if not previsao_df.empty:
        with st.container():
            fig, ax = plt.subplots(figsize=(12, 6))
            sns.lineplot(x='data', y='ocupacao_prevista', data=previsao_df, ax=ax, label='Ocupação Prevista', color='blue')
            ax.set_xlabel("Data", fontsize=12)
            ax.set_ylabel("Ocupação Prevista", fontsize=12)
            ax.set_title(f"Previsão de Ocupação de Leitos - {selected_clinica} ({date(2025, selected_mes, 1).strftime('%B')} 2025)", fontsize=16)
            ax.legend(title="Legenda")
            ax.grid(True, linestyle='--', alpha=0.6)
            plt.xticks(rotation=45)
            st.pyplot(fig)
            st.markdown("<p style='text-align: center;'>Gráfico mostrando a previsão de ocupação de leitos para o mês selecionado em 2025.</p>", unsafe_allow_html=True)

        # Resumo da Análise
        st.markdown("""
        ### Resumo da Análise

        A previsão de ocupação de leitos para a clínica selecionada foi realizada utilizando o modelo ARIMA, com base nos dados históricos dos anos de 2022 a 2024. A análise permite antecipar picos de demanda e planejar a alocação de recursos de forma eficiente. A previsão para o mês selecionado em 2025 é apresentada no gráfico acima.
        """)
    else:
        st.warning("Nenhum dado disponível para os filtros selecionados.")
        st.stop()

# Função para analisar a clusterização de pacientes
def analise_clusterizacao_pacientes(app):
    st.markdown("<hr>", unsafe_allow_html=True)
    st.header("Análise de Clusterização de Pacientes")

    # Proposta da Análise
    st.markdown("""
    ### Proposta da Análise

    A clusterização de pacientes ajuda a agrupar indivíduos com características semelhantes, utilizando informações como idade, frequência de consultas e presença de doenças crônicas. Isso permite:
    - Identificação de grupos de risco.
    - Otimização de alocação de recursos médicos.
    - Personalização de tratamentos para diferentes perfis de pacientes.
    """)

    # Carregar dados dos pacientes
    try:
        with app.app_context():
            session = get_session()
            pacientes = session.query(Paciente.id, Paciente.idade, Paciente.sexo).all()
            atendimentos = session.query(Atendimento.id_paciente, Atendimento.id_doenca).all()
            doencas = session.query(Doenca.id, Doenca.nome).all()
            session.close()

        if not pacientes or not atendimentos or not doencas:
            st.warning("Nenhum dado de paciente, atendimento ou doença disponível.")
            return

        # Preparação dos dados
        df_pacientes = pd.DataFrame(pacientes, columns=["ID", "Idade", "Sexo"])
        df_atendimentos = pd.DataFrame(atendimentos, columns=["ID_Paciente", "ID_Doenca"])
        df_doencas = pd.DataFrame(doencas, columns=["ID_Doenca", "Nome_Doenca"])
        df = df_pacientes.merge(df_atendimentos, left_on="ID", right_on="ID_Paciente")
        df = df.merge(df_doencas, on="ID_Doenca", how="left")

        # Adicionar coluna de frequência de consultas
        df_freq = df.groupby("ID").size().reset_index(name="Frequência_Consultas")
        df = df.merge(df_freq, on="ID")

        # Adicionar coluna de doença crônica
        df["Doença_Crônica"] = df["Nome_Doenca"].apply(lambda x: 1 if pd.notnull(x) else 0)

        if df.empty:
            st.warning("Nenhum dado disponível após a junção dos dados de pacientes, atendimentos e doenças.")
            return

        # --- Normalização ---
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(df[["Idade", "Frequência_Consultas", "Doença_Crônica"]])

        if scaled_data.shape[0] < 2:
            st.warning("Dados insuficientes para aplicar clusterização.")
            return

        # --- K-means ---
        kmeans = KMeans(n_clusters=3, random_state=42)
        df['Cluster_KMeans'] = kmeans.fit_predict(scaled_data)

        # --- DBSCAN ---
        dbscan = DBSCAN(eps=1.2, min_samples=5)
        df['Cluster_DBSCAN'] = dbscan.fit_predict(scaled_data)

        # --- PCA ---
        pca = PCA(n_components=2)
        pca_result = pca.fit_transform(scaled_data)
        df['PCA1'] = pca_result[:, 0]
        df['PCA2'] = pca_result[:, 1]

        # --- Visualização ---
        st.markdown("### Visualização dos Clusters")

        # Gráfico K-means com grade e espaçamento otimizado
        fig_kmeans = plt.figure(figsize=(12, 8))  # Aumenta o tamanho do gráfico
        sns.scatterplot(
            x="PCA1", y="PCA2", hue="Cluster_KMeans", data=df, palette="Set2", s=120, edgecolor="w"
        )
        plt.title(
            "Clusters Identificados pelo K-means", fontsize=20, pad=30
        )  # Título com espaçamento aumentado
        plt.xlabel(
            "Componente Principal 1 (Reduzido por PCA)", fontsize=16, labelpad=20
        )  # Eixo X com espaçamento
        plt.ylabel(
            "Componente Principal 2 (Reduzido por PCA)", fontsize=16, labelpad=20
        )  # Eixo Y com espaçamento
        plt.legend(
            title="Grupos Identificados", loc="upper right", fontsize=12, title_fontsize=14
        )  # Legenda ajustada
        plt.grid(True, linestyle="--", alpha=0.6)  # Adiciona grade com linhas tracejadas e semitransparência
        plt.subplots_adjust(bottom=0.25, top=0.85, left=0.1, right=0.9)  # Ajusta margens para melhor exibição
        plt.annotate(
            "Cada ponto representa um paciente agrupado por semelhanças com base em idade, frequência de consultas e doenças crônicas.\nOs clusters indicam diferentes perfis de pacientes.",
            xy=(0.5, -0.3), xycoords="axes fraction", ha="center", fontsize=12,
            color="dimgray"
        )  # Anotação com espaçamento aumentado e alinhamento centralizado
        st.pyplot(fig_kmeans)

        # Gráfico DBSCAN com grade e espaçamento otimizado
        fig_dbscan = plt.figure(figsize=(12, 8))
        sns.scatterplot(
            x="PCA1", y="PCA2", hue="Cluster_DBSCAN", data=df, palette="Set1", s=120, edgecolor="w"
        )
        plt.title(
            "Clusters Identificados pelo DBSCAN", fontsize=20, pad=30
        )  # Título com espaçamento aumentado
        plt.xlabel(
            "Componente Principal 1 (Reduzido por PCA)", fontsize=16, labelpad=20
        )  # Eixo X com espaçamento
        plt.ylabel(
            "Componente Principal 2 (Reduzido por PCA)", fontsize=16, labelpad=20
        )  # Eixo Y com espaçamento
        plt.legend(
            title="Grupos Identificados", loc="upper right", fontsize=12, title_fontsize=14
        )  # Legenda ajustada
        plt.grid(True, linestyle="--", alpha=0.6)  # Adiciona grade ao gráfico
        plt.subplots_adjust(bottom=0.25, top=0.85, left=0.1, right=0.9)  # Ajusta margens para melhor exibição
        plt.annotate(
            "Os pontos representam pacientes. Clusters identificados pelo algoritmo DBSCAN,\nque agrupa com base na densidade local dos dados e destaca possíveis outliers.",
            xy=(0.5, -0.3), xycoords="axes fraction", ha="center", fontsize=12,
            color="dimgray"
        )  # Anotação centralizada
        st.pyplot(fig_dbscan)


        # --- Resumo ---
        st.markdown("""
        ### Resumo da Análise

        Os gráficos mostram como os pacientes foram agrupados com base em características comuns:
        - **Clusters K-means**:
            - Segmentação em 3 grupos principais com base em padrões.
            - Cada grupo representa um perfil geral de pacientes, como alta idade ou alta frequência de consultas.
        - **Clusters DBSCAN**:
            - Detecta grupos densos e outliers.
            - Os pacientes rotulados como `-1` são considerados fora de padrões comuns.
        """)
    except Exception as e:
        st.error(f"Ocorreu um erro durante a análise: {e}")
