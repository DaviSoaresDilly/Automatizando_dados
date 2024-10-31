# app/reports/generate_reports.py
import sys
import os
import pandas as pd
from sqlalchemy import func
from sqlalchemy.orm import Session
from datetime import datetime, date, timedelta
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from app.models import Atendimento, Clinica, Medico, Paciente, Doenca, Bairro
from app.database import get_session, create_app
from analyze_occupacao_arima import prever_ocupacao_arima, extrair_dados_ocupacao, calcular_ocupacao_media
from app.reports.visualize import plot_ocupacao_historico_previsao, plot_atendimentos_por_clinica, plot_grupo_risco_atendimentos

# Constantes
OUTPUT_DIR = './reports'

# Função para garantir o diretório de saída
def ensure_output_dir():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

# Função para exportar relatórios em CSV e PDF
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

# Função nova: Relatório de ocupação de leitos com previsão
def generate_occupacao_report(session: Session, clinica_id: int, dias_previstos: int = 30) -> pd.DataFrame:
    """
    Gera um relatório de ocupação de leitos para uma clínica específica e realiza uma previsão para um período futuro.
    """
    clinica = session.query(Clinica).filter(Clinica.id == clinica_id).first()
    if clinica is None:
        raise ValueError(f"Clínica com ID {clinica_id} não encontrada.")
    
    data_fim = date.today()
    data_inicio = data_fim - timedelta(days=180)  # Últimos 6 meses
    df_ocupacao = extrair_dados_ocupacao(clinica_id, data_inicio, data_fim)
    ocupacao_media_historica = calcular_ocupacao_media(df_ocupacao, clinica.capacidade_leito)
    
    # Previsão de ocupação
    previsao_df = prever_ocupacao_arima(clinica_id, dias_previstos)
    
    # Dados históricos para visualização
    historico_df = pd.DataFrame({
        "data": ocupacao_media_historica.index,
        "ocupacao": ocupacao_media_historica.values
    })
    
    # Visualização
    plot_ocupacao_historico_previsao(historico_df, previsao_df, clinica.nome)
    
    # Combinação de dados para o relatório final
    relatorio_df = pd.concat([historico_df.set_index("data"), previsao_df.set_index("data")], axis=1)
    relatorio_df.columns = ["Ocupação Histórica", "Ocupação Prevista"]
    relatorio_df.reset_index(inplace=True)
    
    return relatorio_df

# Função nova: Relatório de maior quantidade de doenças por bairro
def generate_doenca_por_bairro_report(session: Session) -> pd.DataFrame:
    """
    Gera um relatório da maior quantidade de doenças por bairro.
    """
    # Consulta para obter a quantidade de doenças por bairro
    query = (
        session.query(Bairro.nome.label('Bairro'), Doenca.nome.label('Doença'), func.count(Atendimento.id).label('Quantidade'))
        .join(Atendimento, Atendimento.id_bairro == Bairro.id)
        .join(Doenca, Atendimento.id_doenca == Doenca.id)
        .group_by(Bairro.nome, Doenca.nome)
        .order_by(Bairro.nome, func.count(Atendimento.id).desc())
    )
    
    # Conversão dos resultados para DataFrame
    df_doenca_por_bairro = pd.read_sql(query.statement, session.bind)
    
    # Visualização
    plot_doenca_por_bairro(df_doenca_por_bairro)
    
    return df_doenca_por_bairro

# Função para plotar a quantidade de doenças por bairro
def plot_doenca_por_bairro(df: pd.DataFrame):
    """
    Gera um gráfico de barras da quantidade de doenças por bairro.
    """
    plt.figure(figsize=(14, 10))
    bairros = df['Bairro'].unique()
    for bairro in bairros:
        subset = df[df['Bairro'] == bairro]
        plt.bar(subset['Doença'], subset['Quantidade'], label=bairro)
    
    plt.xlabel('Doença')
    plt.ylabel('Quantidade')
    plt.title('Quantidade de Doenças por Bairro')
    plt.legend(title='Bairro')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

# Exemplo de uso das funções
if __name__ == "__main__":
    app = create_app()  # Criação da aplicação Flask
    with app.app_context():  # Ativação do contexto da aplicação
        session = get_session()

        # Gerar e exportar relatório de ocupação de leitos
        clinica_id = 1  # ID da clínica de exemplo
        dias_previstos = 30  # Período de previsão em dias
        df_occupacao = generate_occupacao_report(session, clinica_id, dias_previstos)
        
        # Salvar o relatório em CSV e PDF
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        export_to_file(df_occupacao, f'occupacao_report_{clinica_id}_{timestamp}', 'csv')
        export_to_file(df_occupacao, f'occupacao_report_{clinica_id}_{timestamp}', 'pdf')
        
        print(f"Relatório de ocupação de leitos gerado para a clínica com ID {clinica_id}.")