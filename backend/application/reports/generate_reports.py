# application/reports/generate_reports.py

import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from sqlalchemy import and_, func, select
from sqlalchemy.orm import Session
from datetime import datetime, date, timedelta
from application.models import Atendimento, Clinica, Medico, Paciente, Doenca, Bairro
from application.database import get_session, create_app
from analyze_occupacao_arima import (
    prever_ocupacao_arima,
    extrair_dados_ocupacao,
    calcular_ocupacao_media,
    selecionar_melhor_arima,
)
from application.reports.visualize import (
    plot_doenca_por_bairro,
    plot_ocupacao_historico_previsao,
    plot_distribution_by_age_gender,
)

OUTPUT_DIR = './reports'

def ensure_output_dir():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

def export_to_file(df: pd.DataFrame, filename: str, fmt: str = 'csv'):
    ensure_output_dir()
    filepath = os.path.join(OUTPUT_DIR, f"{filename}.{fmt}")
    if fmt == 'csv':
        df.to_csv(filepath, index=False)
    elif fmt == 'pdf':
        from fpdf import FPDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Relatório", ln=True, align='C')
        for _, row in df.iterrows():
            linha = ' | '.join([f"{col}: {row[col]}" for col in df.columns])
            pdf.cell(200, 10, txt=linha, ln=True)
        pdf.output(filepath)
    print(f"Relatório salvo em: {filepath}")

# Função para converter intervalo de data
def calculate_date_range(period: str) -> timedelta:
    if period == "Mensal":
        return timedelta(days=30)
    elif period == "Trimestral":
        return timedelta(days=90)
    elif period == "Anual":
        return timedelta(days=365)
    else:
        raise ValueError("Período inválido. Escolha entre 'Mensal', 'Trimestral' ou 'Anual'.")

# Funções para gerar relatórios
def generate_occupacao_report(session: Session, clinica_id: int, dias_previstos: int = 30, period: str = "Mensal") -> pd.DataFrame:
    clinica = session.query(Clinica).filter(Clinica.id == clinica_id).first()
    if clinica is None:
        raise ValueError(f"Clínica com ID {clinica_id} não encontrada.")
    
    data_fim = date.today()
    data_inicio = data_fim - calculate_date_range(period)
    df_ocupacao = extrair_dados_ocupacao(clinica_id, data_inicio, data_fim)

    if df_ocupacao.empty:
        print("Nenhum dado de ocupação encontrado para o período selecionado.")
        return pd.DataFrame()  # Retorna DataFrame vazio para evitar falhas

    ocupacao_media_historica = calcular_ocupacao_media(df_ocupacao, clinica.capacidade_leito)
    
    all_dates = pd.date_range(start=data_inicio, end=data_fim, freq='D')
    ocupacao_media_historica = ocupacao_media_historica.reindex(all_dates, fill_value=0)
    ocupacao_media_historica.index.freq = 'D'

    previsao_df = prever_ocupacao_arima(clinica_id, dias_previstos)
    
    historico_df = pd.DataFrame({
        "data": ocupacao_media_historica.index,
        "Ocupação Histórica": ocupacao_media_historica.values
    })

    previsao_df.columns = ["data", "Ocupação Prevista"]

    relatorio_df = pd.concat([historico_df.set_index("data"), previsao_df.set_index("data")], axis=1)
    relatorio_df.reset_index(inplace=True)

    return relatorio_df

def generate_doenca_por_bairro_report(session: Session, bairro: str = None, period: str = "Mensal") -> pd.DataFrame:
    data_fim = date.today()
    data_inicio = data_fim - calculate_date_range(period)

    query = (
        select(Bairro.nome.label("Bairro"), Doenca.nome.label("Doença"), func.count(Atendimento.id).label("Quantidade"))
        .join(Atendimento, Atendimento.id_bairro == Bairro.id)
        .join(Doenca, Atendimento.id_doenca == Doenca.id)
        .filter(and_(Atendimento.data_atendimento >= data_inicio, Atendimento.data_atendimento <= data_fim))
        .group_by(Bairro.nome, Doenca.nome)
        .order_by(Bairro.nome, func.count(Atendimento.id).desc())
    )
    if bairro:
        query = query.filter(Bairro.nome == bairro)

    result = session.execute(query).fetchall()
    df_doenca_por_bairro = pd.DataFrame(result, columns=["Bairro", "Doença", "Quantidade"])
    
    fig, ax = plt.subplots(figsize=(14, 10))
    plot_doenca_por_bairro(df_doenca_por_bairro, fig, ax)

    output_path = f"./reports/doenca_por_bairro.png"
    plt.savefig(output_path)
    print(f"Gráfico salvo em: {output_path}")

    return df_doenca_por_bairro

def generate_age_gender_distribution_report(session: Session, genero: str = None, faixa_etaria: str = None, period: str = "Mensal") -> pd.DataFrame:
    data_fim = date.today()
    data_inicio = data_fim - calculate_date_range(period)

    query = (
        session.query(Paciente, Atendimento, Doenca)
        .join(Atendimento, Paciente.id == Atendimento.id_paciente)
        .join(Doenca, Atendimento.id_doenca == Doenca.id)
        .filter(and_(Atendimento.data_atendimento >= data_inicio, Atendimento.data_atendimento <= data_fim))
    )

    if genero != "Todos":
        query = query.filter(Paciente.sexo == genero)

    dados = [
        {
            "Paciente": paciente.nome,
            "Idade": paciente.idade,
            "Sexo": paciente.sexo,
            "Doenca": doenca.nome,
        }
        for paciente, atendimento, doenca in query.all()
    ]

    df = pd.DataFrame(dados)
    if df.empty:
        print("Nenhum dado encontrado para os filtros selecionados.")
        return pd.DataFrame()  # Evita erros ao retornar DataFrame vazio

    df["Faixa Etária"] = pd.cut(df["Idade"], bins=[0, 12, 18, 40, 60, 100], labels=["Criança", "Adolescente", "Adulto", "Meia-Idade", "Idoso"])

    distribuicao_df = df.groupby(["Faixa Etária", "Sexo", "Doenca"]).size().reset_index(name="Incidências")
    return distribuicao_df

# Função para gerar relatório de ocupação de leitos com filtro de clínica e período
def generate_filtered_occupacao_report(session, clinica_nome, period):
    clinica = session.query(Clinica).filter(Clinica.nome == clinica_nome).first()  # Obter objeto completo da clínica
    if clinica is None:
        raise ValueError(f"Clínica '{clinica_nome}' não encontrada.")

    data_fim = date.today()
    data_inicio = data_fim - calculate_date_range(period)
    df_ocupacao = extrair_dados_ocupacao(clinica.id, data_inicio, data_fim)

    if df_ocupacao.empty:
        return pd.DataFrame()  # Retorna vazio para evitar falhas

    ocupacao_media_historica = calcular_ocupacao_media(df_ocupacao, clinica.capacidade_leito)
    all_dates = pd.date_range(start=data_inicio, end=data_fim, freq='D')
    ocupacao_media_historica = ocupacao_media_historica.reindex(all_dates, fill_value=0)
    ocupacao_media_historica.index.freq = 'D'
    previsao_df = prever_ocupacao_arima(clinica.id, 30)
    
    historico_df = pd.DataFrame({"data": ocupacao_media_historica.index, "Ocupação Histórica": ocupacao_media_historica.values})
    previsao_df.columns = ["data", "Ocupação Prevista"]

    relatorio_df = pd.concat([historico_df.set_index("data"), previsao_df.set_index("data")], axis=1).reset_index()
    return relatorio_df

# Função para gerar relatório de distribuição por idade e gênero com filtros específicos
def generate_filtered_age_gender_distribution_report(session, genero="Todos", faixa_etaria=None, period="Mensal"):
    data_fim = date.today()
    data_inicio = data_fim - calculate_date_range(period)
    
    # Realiza a consulta inicial e registra o período para depuração
    print(f"Consultando dados de {data_inicio} a {data_fim}")
    query = (
        session.query(Paciente.idade, Paciente.sexo, Doenca.nome.label("Doenca"))
        .join(Atendimento, Paciente.id == Atendimento.id_paciente)
        .join(Doenca, Atendimento.id_doenca == Doenca.id)
        .filter(and_(Atendimento.data_atendimento >= data_inicio, Atendimento.data_atendimento <= data_fim))
    )

    # Filtro condicional para gênero e registro para depuração
    if genero != "Todos":
        query = query.filter(Paciente.sexo == genero)
        print(f"Aplicando filtro de gênero: {genero}")

    # Executa a consulta e converte para DataFrame
    dados = [{"Idade": idade, "Sexo": sexo, "Doenca": doenca} for idade, sexo, doenca in query.all()]
    df = pd.DataFrame(dados)
    
    # Verificação de DataFrame vazio após a consulta
    if df.empty:
        print("Nenhum dado retornado pela consulta inicial.")
        return pd.DataFrame()  # Evita erros ao retornar um DataFrame vazio

    # Cria coluna "Faixa Etária" e registra para depuração
    df["Faixa Etária"] = pd.cut(df["Idade"], bins=[0, 12, 18, 40, 60, 100], labels=["Criança", "Adolescente", "Adulto", "Meia-Idade", "Idoso"])
    print(f"Distribuição inicial de faixa etária:\n{df['Faixa Etária'].value_counts()}")

    # Filtro opcional de faixa_etaria
    if faixa_etaria:
        df = df[df["Faixa Etária"] == faixa_etaria]
        print(f"Aplicando filtro de faixa etária: {faixa_etaria}")

    # Verifica se ainda há dados após a aplicação de filtros
    if df.empty:
        print("Nenhum dado disponível após aplicar filtros adicionais.")
        return pd.DataFrame()

    # Gera o DataFrame final de distribuição
    distribuicao_df = df.groupby(["Faixa Etária", "Sexo", "Doenca"], observed=False).size().reset_index(name="Incidências")
    print("Distribuição final gerada com sucesso.")
    
    return distribuicao_df

# Função para gerar relatório de distribuição de doenças por bairro com filtros de doença, bairro e período
def generate_filtered_doenca_por_bairro_report(session, selected_doenca, selected_bairro, date_range):
    data_fim = date.today()
    data_inicio = data_fim - calculate_date_range(date_range)
    
    query = (
        select(Bairro.nome.label("Bairro"), Doenca.nome.label("Doença"), func.count(Atendimento.id).label("Quantidade"))
        .join(Atendimento, Atendimento.id_bairro == Bairro.id)
        .join(Doenca, Atendimento.id_doenca == Doenca.id)
        .filter(and_(Atendimento.data_atendimento >= data_inicio, Atendimento.data_atendimento <= data_fim))
        .group_by(Bairro.nome, Doenca.nome)
        .order_by(Bairro.nome, func.count(Atendimento.id).desc())
    )

    if selected_doenca != "Todas":
        query = query.filter(Doenca.nome == selected_doenca)
    if selected_bairro != "Todos":
        query = query.filter(Bairro.nome == selected_bairro)

    result = session.execute(query).fetchall()
    return pd.DataFrame(result, columns=["Bairro", "Doença", "Quantidade"])

# Função principal
if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        session = get_session()

        clinica_id = 1
        dias_previstos = 30
        period = "Mensal"
        bairro = None
        doenca = None

        df_occupacao = generate_occupacao_report(session, clinica_id, dias_previstos, period)
        df_distribuicao = generate_age_gender_distribution_report(session, doenca, period)
        df_doenca_bairro = generate_doenca_por_bairro_report(session, bairro, period)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        export_to_file(df_occupacao, f'occupacao_report_{clinica_id}_{timestamp}', 'csv')
        export_to_file(df_occupacao, f'occupacao_report_{clinica_id}_{timestamp}', 'pdf')
        export_to_file(df_distribuicao, f'distribuicao_faixa_etaria_sexo_{timestamp}', 'csv')
        export_to_file(df_distribuicao, f'distribuicao_faixa_etaria_sexo_{timestamp}', 'pdf')
        export_to_file(df_doenca_bairro, f'doenca_por_bairro_{timestamp}', 'csv')
        export_to_file(df_doenca_bairro, f'doenca_por_bairro_{timestamp}', 'pdf')