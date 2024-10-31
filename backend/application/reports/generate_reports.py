# app/reports/generate_reports.py

import sys
import os
import pandas as pd
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from datetime import datetime, date, timedelta
import matplotlib.pyplot as plt
import seaborn as sns

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from application.models import Atendimento, Clinica, Medico, Paciente, Doenca, Bairro
from application.database import get_session, create_app
from analyze_occupacao_arima import prever_ocupacao_arima, extrair_dados_ocupacao, calcular_ocupacao_media
from application.reports.visualize import plot_ocupacao_historico_previsao, plot_distribution_by_age_gender

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

def generate_occupacao_report(session: Session, clinica_id: int, dias_previstos: int = 30) -> pd.DataFrame:
    clinica = session.query(Clinica).filter(Clinica.id == clinica_id).first()
    if clinica is None:
        raise ValueError(f"Clínica com ID {clinica_id} não encontrada.")
    
    data_fim = date.today()
    data_inicio = data_fim - timedelta(days=180)
    df_ocupacao = extrair_dados_ocupacao(clinica_id, data_inicio, data_fim)
    ocupacao_media_historica = calcular_ocupacao_media(df_ocupacao, clinica.capacidade_leito)
    
    # Converter o índice para DateTimeIndex
    ocupacao_media_historica.index = pd.to_datetime(ocupacao_media_historica.index)

    previsao_df = prever_ocupacao_arima(clinica_id, dias_previstos)
    
    historico_df = pd.DataFrame({
        "data": ocupacao_media_historica.index,
        "ocupacao": ocupacao_media_historica.values
    })
    
    plot_ocupacao_historico_previsao(historico_df, previsao_df, clinica.nome)
    
    relatorio_df = pd.concat([historico_df.set_index("data"), previsao_df.set_index("data")], axis=1)
    relatorio_df.columns = ["Ocupação Histórica", "Ocupação Prevista"]
    relatorio_df.reset_index(inplace=True)
    
    return relatorio_df


def generate_doenca_por_bairro_report(session: Session) -> pd.DataFrame:
    query = (
        select(
            Bairro.nome.label('Bairro'),
            Doenca.nome.label('Doença'),
            func.count(Atendimento.id).label('Quantidade')
        )
        .join(Atendimento, Atendimento.id_bairro == Bairro.id)
        .join(Doenca, Atendimento.id_doenca == Doenca.id)
        .group_by(Bairro.nome, Doenca.nome)
        .order_by(Bairro.nome, func.count(Atendimento.id).desc())
    )
    
    result = session.execute(query).fetchall()
    df_doenca_por_bairro = pd.DataFrame(result, columns=['Bairro', 'Doença', 'Quantidade'])
    plot_doenca_por_bairro(df_doenca_por_bairro)
    return df_doenca_por_bairro

def plot_doenca_por_bairro(df_doenca_bairro: pd.DataFrame):
    plt.figure(figsize=(14, 10))
    sns.barplot(data=df_doenca_bairro, x='Doença', y='Quantidade', hue='Bairro', errorbar=None)
    
    plt.xlabel('Doença')
    plt.ylabel('Quantidade')
    plt.title('Quantidade de Doenças por Bairro')
    plt.legend(title='Bairro')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    output_path = os.path.join(OUTPUT_DIR, "doenca_por_bairro.png")
    plt.savefig(output_path)
    plt.show()
    print(f"Gráfico salvo em: {output_path}")

def generate_age_gender_distribution_report(session: Session) -> pd.DataFrame:
    query = session.query(Paciente, Atendimento, Doenca, Bairro)\
        .join(Atendimento, Paciente.id == Atendimento.id_paciente)\
        .join(Doenca, Atendimento.id_doenca == Doenca.id)\
        .join(Bairro, Atendimento.id_bairro == Bairro.id)\
        .all()

    dados = [{
        'Paciente': paciente.nome,
        'Idade': paciente.idade,
        'Sexo': paciente.sexo,
        'Doenca': doenca.nome,
        'Gravidade': doenca.gravidade,
        'Bairro': bairro.nome
    } for paciente, atendimento, doenca, bairro in query]

    df = pd.DataFrame(dados)

    df['Faixa Etária'] = pd.cut(
        df['Idade'], 
        bins=[0, 12, 18, 40, 60, 100], 
        labels=['Criança', 'Adolescente', 'Adulto', 'Meia-Idade', 'Idoso']
    )

    distribuicao_df = df.groupby(['Faixa Etária', 'Sexo', 'Doenca'], observed=False).size().reset_index(name='Incidências')
    plot_distribution_by_age_gender(distribuicao_df)
    return distribuicao_df

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        session = get_session()

        clinica_id = 1
        dias_previstos = 30
        df_occupacao = generate_occupacao_report(session, clinica_id, dias_previstos)
        df_distribuicao = generate_age_gender_distribution_report(session)
        df_doenca_bairro = generate_doenca_por_bairro_report(session)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        export_to_file(df_occupacao, f'occupacao_report_{clinica_id}_{timestamp}', 'csv')
        export_to_file(df_occupacao, f'occupacao_report_{clinica_id}_{timestamp}', 'pdf')
        export_to_file(df_distribuicao, f'distribuicao_faixa_etaria_sexo_{timestamp}', 'csv')
        export_to_file(df_distribuicao, f'distribuicao_faixa_etaria_sexo_{timestamp}', 'pdf')
        export_to_file(df_doenca_bairro, f'doenca_por_bairro_{timestamp}', 'csv')
        export_to_file(df_doenca_bairro, f'doenca_por_bairro_{timestamp}', 'pdf')

        print(f"Relatório de ocupação de leitos gerado para a clínica com ID {clinica_id}.")
        print("Relatório de distribuição por faixa etária e sexo gerado.")
        print("Relatório de quantidade de doenças por bairro gerado.")
