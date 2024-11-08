# application/reports/descriptive_analysis.py

from datetime import datetime
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

    # Verificação se o DataFrame não está vazio
    if not df.empty:
        print(f"Número de registros carregados: {len(df)}")

        with st.container():
            # Criação do layout de grade
            col1, col2 = st.columns([0.4, 0.6])

            with col1:
                # Exibição da tabela de dados
                st.markdown(f"<h3 style='text-align: center;'>Tabela de Dados - {selected_ano}</h3>", unsafe_allow_html=True)
                st.dataframe(df)

            with col2:
                # Criação do Heatmap
                period_label = get_period_label(selected_period, data_inicio, data_fim)
                st.markdown(f"<h3 style='text-align: center;'>Distribuição de Doenças - {period_label}</h3>", unsafe_allow_html=True)

                # Criação de uma tabela de contagem para o heatmap
                df_pivot = pd.pivot_table(
                    df,
                    values="Doenca",
                    index="Faixa Etária",
                    columns="Sexo",
                    aggfunc="count",
                    fill_value=0
                )

                fig, ax = plt.subplots(figsize=(12, 8))

                # Heatmap com customização de cores e anotações
                heatmap = sns.heatmap(
                    df_pivot, 
                    annot=True, 
                    fmt="d", 
                    cmap="YlGnBu",  
                    cbar=True, 
                    ax=ax, 
                    linewidths=0.5,  
                    linecolor='gray',
                    cbar_kws={'label': 'Número de Casos'}
                )
                
                # Configurações do Colorbar
                colorbar = heatmap.collections[0].colorbar
                colorbar.ax.tick_params(labelsize=14)  # Define fontsize dos ticks do colorbar
                colorbar.set_label("Número de Casos", fontsize=18, labelpad=20)  # Define fontsize do label do colorbar

                # Personalização dos eixos e título com espaçamento
                ax.set_title("Mapa de Calor", fontsize=20, weight='bold')
                ax.set_xlabel("Gênero", fontsize=18, labelpad=20)  # Espaço extra entre eixo X e o gráfico
                ax.set_ylabel("Faixa Etária", fontsize=18, labelpad=20)  # Espaço extra entre eixo Y e o gráfico
                ax.tick_params(axis='both', labelsize=14)
                plt.xticks(ha='right')  # Rotação dos rótulos do eixo X

                # Ajuste do tamanho do texto das anotações
                for text in heatmap.texts:
                    text.set_size(14)

                # Ajuste automático do layout para evitar sobreposição
                plt.tight_layout()

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
    st.markdown("<hr>", unsafe_allow_html=True)

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
        especialidades = get_especialidades_list(session)
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
        period_label = get_period_label(selected_period, data_inicio, data_fim)
        doencas = get_doencas_por_especialidade(session, selected_especialidade)
        df = fetch_data_bairros(session, selected_period, selected_ano, selected_mes, selected_trimestre, doencas, selected_bairro)
        session.close()

    # Verifica se o DataFrame não está vazio
    if not df.empty:
        # Log para verificar o número de registros carregados
        print(f"Número de registros carregados: {len(df)}")

        # Dividir os bairros em dois grupos
        bairros_list = df['Bairro'].unique()
        mid_index = len(bairros_list) // 2
        bairros_grupo1 = bairros_list[:mid_index]
        bairros_grupo2 = bairros_list[mid_index:]

        # Filtrar os dados para cada grupo de bairros
        df_grupo1 = df[df['Bairro'].isin(bairros_grupo1)]
        df_grupo2 = df[df['Bairro'].isin(bairros_grupo2)]

        # Layout para o Grupo 1
        with st.container():
            # Margem para a próxima análise
            st.markdown("<br><br>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='text-align: center;'>Distribuição de Doenças por Bairros - {period_label}</h3>", unsafe_allow_html=True)

            # Contagem de casos por bairro e doença para o Grupo 1
            df_count_grupo1 = df_grupo1.groupby(['Bairro', 'Doenca']).size().reset_index(name='Casos')

            # Criação do gráfico de bolhas para o Grupo 1
            fig, ax = plt.subplots(figsize=(12, 6))
            scatter = ax.scatter(
                x=df_count_grupo1['Bairro'],
                y=df_count_grupo1['Doenca'],
                s=df_count_grupo1['Casos'] * 150,  # Ajuste do tamanho das bolhas
                alpha=0.6,
                edgecolors="gray",
                linewidth=0.5,
                c=df_count_grupo1['Casos'], cmap='viridis'  # Paleta de cores para as bolhas
            )
            
            # Anotação dos valores de casos nas bolhas
            for i in range(len(df_count_grupo1)):
                ax.annotate(df_count_grupo1['Casos'][i], 
                            (df_count_grupo1['Bairro'][i], df_count_grupo1['Doenca'][i]), 
                            color='black', weight='bold', fontsize=8, ha='center', va='center')
            
            # Configurações de rótulos e título
            ax.set_xlabel("Bairro", fontsize=12)
            ax.set_ylabel("Doença", fontsize=12)
            ax.set_title("Distribuição de Doenças por Bairros - Grupo 1", fontsize=16)
            plt.xticks(rotation=45)
            plt.grid(True, linestyle='--', alpha=0.5)
            
            # Adicionando uma barra de cores (colorbar) para indicar o número de casos
            cbar = plt.colorbar(scatter)
            cbar.set_label('Número de Casos')

            st.pyplot(fig)

        # Layout para o Grupo 2
        with st.container():
            st.markdown("<br><br>", unsafe_allow_html=True)
            
            # Contagem de casos por bairro e doença para o Grupo 2
            df_count_grupo2 = df_grupo2.groupby(['Bairro', 'Doenca']).size().reset_index(name='Casos')

            # Criação do gráfico de bolhas para o Grupo 2
            fig, ax = plt.subplots(figsize=(12, 6))
            scatter = ax.scatter(
                x=df_count_grupo2['Bairro'],
                y=df_count_grupo2['Doenca'],
                s=df_count_grupo2['Casos'] * 150,
                alpha=0.6,
                edgecolors="gray",
                linewidth=0.5,
                c=df_count_grupo2['Casos'], cmap='cool'  # Paleta de cores
            )

            # Anotação dos valores de casos nas bolhas
            for i in range(len(df_count_grupo2)):
                ax.annotate(df_count_grupo2['Casos'][i], 
                            (df_count_grupo2['Bairro'][i], df_count_grupo2['Doenca'][i]), 
                            color='black', weight='bold', fontsize=8, ha='center', va='center')
            
            # Configurações de rótulos e título
            ax.set_xlabel("Bairro", fontsize=12)
            ax.set_ylabel("Doença", fontsize=12)
            ax.set_title("Distribuição de Doenças por Bairros - Grupo 2", fontsize=16)
            plt.xticks(rotation=45)
            plt.grid(True, linestyle='--', alpha=0.5)
            
            # Adicionando uma barra de cores para indicar o número de casos
            cbar = plt.colorbar(scatter)
            cbar.set_label('Número de Casos')

            st.pyplot(fig)

        # Gerar Relatório
        if st.button("Gerar Relatório", key="gerar_relatorio_bairros"):
            analysis_summary = (
                "Esta análise mostra a distribuição de doenças por bairros. "
                "Observa-se que determinados bairros têm uma incidência maior de doenças, "
                "o que pode indicar a necessidade de intervenções específicas nessas áreas."
            )
            output_path_pdf = f'relatorio_incidencia_bairros_{selected_ano}.pdf'
            output_path_csv = f'tabela_incidencia_bairros_{selected_ano}.csv'
            generate_report(df, analysis_summary, output_path_pdf, output_path_csv, selected_ano)
            st.success(f"Relatório gerado com sucesso: {os.path.join('reports', output_path_pdf)}")
            st.success(f"Tabela de dados gerada com sucesso: {os.path.join('reports', output_path_csv)}")
    else:
        st.warning("Nenhum dado disponível para os filtros selecionados.")
        st.stop()

# so quebra de linha    