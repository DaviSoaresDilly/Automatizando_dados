# application/reports/descriptive_analysis.py

from datetime import datetime
import geopandas as gpd
import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from application.database import get_session
from data_fetcher import get_doenca_list, fetch_data, get_bairros_list, fetch_data_bairros, get_doencas_por_especialidade, get_especialidades_list
from date_utils import calculate_date_range, get_period_label
from report_generator import generate_report

# Função para realizar a análise descritiva de distribuição de doenças
def analise_distribuicao_doenca(app):
    st.header("Análise Descritiva de distribuição de doenças")

    # Proposta da Análise
    st.markdown("""
    ### Proposta da Análise

    A análise descritiva é uma abordagem fundamental na análise de dados que se concentra em resumir e descrever as características principais de um conjunto de dados. No contexto da saúde pública, a análise descritiva pode ser usada para entender melhor a distribuição de doenças por faixa etária, gênero e outros fatores demográficos. Esta análise ajuda a identificar padrões e tendências que podem ser críticos para a tomada de decisões informadas e para o planejamento estratégico.

    **Benefícios da Análise**:
    - **Identificação de Padrões**: A análise descritiva permite identificar padrões na distribuição de doenças, como quais faixas etárias ou gêneros são mais afetados por determinadas doenças.
    - **Planejamento de Recursos**: Compreender a distribuição de doenças ajuda na alocação eficiente de recursos, como profissionais de saúde, medicamentos e equipamentos.
    - **Prevenção e Controle**: Identificar grupos de risco pode ajudar na implementação de medidas preventivas e de controle mais eficazes.
    - **Tomada de Decisões Informadas**: Fornece uma base sólida de dados para apoiar decisões estratégicas em saúde pública.
    """)

    # Carregar dados para o filtro de doenças
    with app.app_context():
        session = get_session()
        # Popula a lista de doenças
        doencas = ["Todas"] + get_doenca_list(session)
        session.close()

    # Menu de Filtros
    st.sidebar.header("Filtros - Distribuição de Doenças")
    selected_period = st.sidebar.selectbox("Período", ["Mensal", "Trimestral", "Anual"], index=2, key="periodo_distribuicao")
    selected_ano = st.sidebar.selectbox("Ano", list(range(2022, 2025)), index=2, key="ano_distribuicao")
    selected_mes = st.sidebar.selectbox("Mês", list(range(1, 13)), format_func=lambda x: datetime(2022, x, 1).strftime('%B'), key="mes_distribuicao") if selected_period == "Mensal" else None
    selected_trimestre = st.sidebar.selectbox("Trimestre", ["1º Trimestre", "2º Trimestre", "3º Trimestre", "4º Trimestre"], key="trimestre_distribuicao") if selected_period == "Trimestral" else None
    selected_doenca = st.sidebar.selectbox("Doença", doencas, key="doenca_distribuicao")
    selected_genero = st.sidebar.selectbox("Gênero", ["Todos", "M", "F"], key="genero_distribuicao")
    selected_faixa_etaria = st.sidebar.selectbox("Faixa Etária", ["Todas", "Criança", "Adolescente", "Adulto", "Meia-Idade", "Idoso"], key="faixa_etaria_distribuicao")

    # Busca os dados com base nos filtros selecionados
    with app.app_context():
        session = get_session()
        data_inicio, data_fim = calculate_date_range(selected_period, selected_ano, selected_mes, selected_trimestre)
        df = fetch_data(session, selected_period, selected_ano, selected_mes, selected_trimestre, selected_doenca, selected_genero, selected_faixa_etaria)
        session.close()

    # Verifica se o DataFrame não está vazio
    if not df.empty:
        # Log para verificar o número de registros carregados
        print(f"Número de registros carregados: {len(df)}")

        # Criação do layout de grade
        col1, col2 = st.columns(2)

        with col1:
            # Exibição da tabela de dados
            st.subheader("Tabela de Dados")
            st.dataframe(df)

        with col2:
            # Criação do Heatmap
            period_label = get_period_label(selected_period, data_inicio, data_fim)
            st.subheader(f"Distribuição de Doenças por Faixa Etária e Gênero - {period_label}")

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
            sns.heatmap(df_pivot, annot=True, fmt="d", cmap="coolwarm", cbar=True, ax=ax)
            ax.set_title(f"Mapa de Calor")
            st.pyplot(fig)

        # Gerar Relatório
        if st.button("Gerar Relatório"):
            analysis_summary = (
                "Esta análise mostra a distribuição de doenças por faixa etária e gênero. "
                "Observa-se que a gripe é mais comum em crianças e idosos, enquanto a Covid "
                "é mais prevalente em adolescentes e adultos."
            )
            period_label = selected_ano
            output_path_pdf = f'relatorio_analise_{period_label}.pdf'
            output_path_csv = f'tabela_dados_{period_label}.csv'
            generate_report(df, analysis_summary, output_path_pdf, output_path_csv, period_label)
            st.success(f"Relatório gerado com sucesso: {os.path.join('reports', output_path_pdf)}")
            st.success(f"Tabela de dados gerada com sucesso: {os.path.join('reports', output_path_csv)}")
    else:
        st.warning("Nenhum dado disponível para os filtros selecionados.")
        st.stop()

# Função para realizar a análise descritiva de incidência de doenças por bairros
def analise_incidencia_bairros(app):
    st.header("Análise Descritiva de Incidência de Doenças por Bairros")

    # Proposta da Análise
    st.markdown("""
    ### Proposta da Análise

    A análise descritiva de incidência de doenças por bairros se concentra em entender a distribuição geográfica das doenças. No contexto da saúde pública, essa análise pode ser usada para identificar áreas de maior risco e necessidade de intervenção. Esta análise ajuda a identificar padrões e tendências que podem ser críticos para a tomada de decisões informadas e para o planejamento estratégico.

    **Benefícios da Análise**:
    - **Identificação de Áreas de Risco**: A análise permite identificar bairros com maior incidência de doenças.
    - **Planejamento de Recursos**: Compreender a distribuição geográfica das doenças ajuda na alocação eficiente de recursos, como profissionais de saúde, medicamentos e equipamentos.
    - **Prevenção e Controle**: Identificar áreas de risco pode ajudar na implementação de medidas preventivas e de controle mais eficazes.
    - **Tomada de Decisões Informadas**: Fornece uma base sólida de dados para apoiar decisões estratégicas em saúde pública.
    """)

    # Carregar dados para o filtro de especialidades e bairros
    with app.app_context():
        session = get_session()
        # Popula a lista de especialidades e bairros
        especialidades = ["Todas"] + get_especialidades_list(session)
        bairros = ["Todos"] + get_bairros_list(session)
        session.close()

    # Menu de Filtros
    st.sidebar.header("Filtros - Incidência por Bairros")
    selected_period = st.sidebar.selectbox("Período", ["Mensal", "Trimestral", "Anual"], index=2, key="periodo_bairros")
    selected_ano = st.sidebar.selectbox("Ano", list(range(2022, 2025)), index=2, key="ano_bairros")
    selected_mes = st.sidebar.selectbox("Mês", list(range(1, 13)), format_func=lambda x: datetime(2022, x, 1).strftime('%B'), key="mes_bairros") if selected_period == "Mensal" else None
    selected_trimestre = st.sidebar.selectbox("Trimestre", ["1º Trimestre", "2º Trimestre", "3º Trimestre", "4º Trimestre"], key="trimestre_bairros") if selected_period == "Trimestral" else None
    selected_especialidade = st.sidebar.selectbox("Especialidade", especialidades, key="especialidade_bairros")
    selected_bairro = st.sidebar.selectbox("Bairro", bairros, key="bairro_bairros")

    # Busca os dados com base nos filtros selecionados
    with app.app_context():
        session = get_session()
        data_inicio, data_fim = calculate_date_range(selected_period, selected_ano, selected_mes, selected_trimestre)
        doencas = get_doencas_por_especialidade(session, selected_especialidade)
        df = fetch_data_bairros(session, selected_period, selected_ano, selected_mes, selected_trimestre, doencas, selected_bairro)
        session.close()

    # Verifica se o DataFrame não está vazio
    if not df.empty:
        # Log para verificar o número de registros carregados
        print(f"Número de registros carregados: {len(df)}")

        # Criação do layout de grade
        col1, col2 = st.columns(2)

        with col1:
            # Criação do Mapa de Bairros
            period_label = get_period_label(selected_period, data_inicio, data_fim)
            st.subheader(f"Distribuição de Doenças por Bairros - {period_label}")

            # Carregar o shapefile dos bairros (substitua 'path_to_shapefile' pelo caminho correto)
            shapefile_path = 'caminho/para/seu/shapefile.shp'  # Substitua pelo caminho correto
            gdf_bairros = gpd.read_file(shapefile_path)

            # Contagem de casos por bairro
            df_count = df.groupby('Bairro').size().reset_index(name='Casos')

            # Mesclar os dados de contagem com o GeoDataFrame dos bairros
            gdf_bairros = gdf_bairros.merge(df_count, left_on='nome_bairro', right_on='Bairro', how='left').fillna(0)

            # Plotar o mapa
            fig, ax = plt.subplots(1, 1, figsize=(10, 6))
            gdf_bairros.plot(column='Casos', ax=ax, legend=True, cmap='OrRd', legend_kwds={'label': "Número de Casos"})
            plt.title(f"Distribuição de Doenças por Bairros - {period_label}")
            plt.xlabel("Longitude")
            plt.ylabel("Latitude")
            st.pyplot(fig)

        with col2:
            # Criação do Gráfico de Barras
            st.subheader(f"Distribuição de Doenças por Especialidade - {period_label}")

            # Criação de uma tabela de contagem para o gráfico de barras
            df_count = df.groupby(['Bairro', 'Doenca']).size().unstack(fill_value=0)

            df_count.plot(kind='bar', stacked=True, figsize=(10, 6))
            plt.title(f"Distribuição de Doenças por Especialidade - {period_label}")
            plt.xlabel("Bairro")
            plt.ylabel("Número de Casos")
            plt.xticks(rotation=45)
            plt.legend(title="Doença")
            st.pyplot(plt)

        # Gerar Relatório
        if st.button("Gerar Relatório", key="gerar_relatorio_bairros"):
            analysis_summary = (
                "Esta análise mostra a distribuição de doenças por bairros. "
                "Observa-se que determinados bairros têm uma incidência maior de doenças, "
                "o que pode indicar a necessidade de intervenções específicas nessas áreas."
            )
            period_label = selected_ano
            output_path_pdf = f'relatorio_incidencia_bairros_{period_label}.pdf'
            output_path_csv = f'tabela_incidencia_bairros_{period_label}.csv'
            generate_report(df, analysis_summary, output_path_pdf, output_path_csv, period_label)
            st.success(f"Relatório gerado com sucesso: {os.path.join('reports', output_path_pdf)}")
            st.success(f"Tabela de dados gerada com sucesso: {os.path.join('reports', output_path_csv)}")
    else:
        st.warning("Nenhum dado disponível para os filtros selecionados.")
        st.stop()

# so quebra de linha    