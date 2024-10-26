# app/reports/generate_reports.py
import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models import Atendimento, Clinica, Medico, Paciente, Doenca, Bairro
from datetime import datetime
from app.database import get_session, create_app
from app.reports.visualize import plot_atendimentos_por_clinica, plot_grupo_risco_atendimentos

# Função existente: Relatório de atendimentos por clínica
def generate_atendimentos_report(session: Session) -> pd.DataFrame:
    atendimentos = session.query(Atendimento).all()
    clinicas = session.query(Clinica).all()

    data = []
    for clinica in clinicas:
        atendimentos_por_clinica = session.query(Atendimento).filter_by(id_clinica=clinica.id).count()
        data.append({'Clinica': clinica.nome, 'Total Atendimentos': atendimentos_por_clinica})

    df = pd.DataFrame(data)
    return df

# Função existente: Relatório paginado de atendimentos
def generate_atendimentos_report_paginated(session, page: int = 1, per_page: int = 50) -> pd.DataFrame:
    offset = (page - 1) * per_page
    atendimentos = session.query(Atendimento).offset(offset).limit(per_page).all()

    data = []
    for atendimento in atendimentos:
        data.append({'Clinica': atendimento.clinica.nome, 'Paciente': atendimento.paciente.nome, 'Status': atendimento.status})

    df = pd.DataFrame(data)
    return df

# Função nova: Relatório demográfico com incidência de doenças por faixa etária e sexo
def generate_demographic_report(session: Session) -> pd.DataFrame:
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

    # Análise por faixa etária e sexo
    df['Faixa Etária'] = pd.cut(df['Idade'], bins=[0, 12, 18, 40, 60, 100], labels=['Criança', 'Adolescente', 'Adulto', 'Meia-Idade', 'Idoso'])
    analise_por_faixa = df.groupby(['Faixa Etária', 'Sexo', 'Doenca'], observed=False).size().reset_index(name='Incidências')

    return analise_por_faixa

# Função nova: Relatório de atendimentos por médico
def generate_atendimentos_por_medico_report(session: Session) -> pd.DataFrame:
    """
    Gera um relatório de atendimentos por médico.
    """
    query = session.query(
        Medico.nome.label('Medico'),
        Medico.especialidade.label('Especialidade'),
        func.count(Atendimento.id).label('Total_Atendimentos')
    ).join(Atendimento, Medico.id == Atendimento.id_medico)\
     .group_by(Medico.id)\
     .all()

    dados = [{
        'Medico': row[0],
        'Especialidade': row[1],
        'Total Atendimentos': row[2]
    } for row in query]

    df = pd.DataFrame(dados)
    return df

# Funções de exportação (CSV e PDF) para qualquer DataFrame gerado
def export_report_to_csv(df: pd.DataFrame, filename: str, output_dir: str = './reports'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    filepath = os.path.join(output_dir, filename)
    df.to_csv(filepath, index=False)
    print(f"Relatório salvo em: {filepath}")

def export_report_to_pdf(df: pd.DataFrame, filename: str, output_dir: str = './reports'):
    from fpdf import FPDF

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    filepath = os.path.join(output_dir, filename)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Relatório", ln=True, align='C')

    for index, row in df.iterrows():
        linha = ' | '.join([f"{col}: {str(row[col])}" for col in df.columns])
        pdf.cell(200, 10, txt=linha, ln=True)

    pdf.output(filepath)
    print(f"Relatório salvo em: {filepath}")

# Exemplo de uso das funções
if __name__ == "__main__":
    app = create_app()  # Crie a aplicação Flask
    with app.app_context():  # Ative o contexto da aplicação
        session = get_session()

        # Gerar e exportar relatório de atendimentos por clínica
        df_atendimentos = generate_atendimentos_report(session)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        export_report_to_csv(df_atendimentos, f'atendimentos_report_{timestamp}.csv')
        export_report_to_pdf(df_atendimentos, f'atendimentos_report_{timestamp}.pdf')
        plot_atendimentos_por_clinica(df_atendimentos, f'./reports/atendimentos_por_clinica_{timestamp}.png')

        # Gerar e exportar relatório demográfico
        df_demografico = generate_demographic_report(session)
        export_report_to_csv(df_demografico, f'demographic_report_{timestamp}.csv')
        export_report_to_pdf(df_demografico, f'demographic_report_{timestamp}.pdf')

        # Gerar e exportar relatório de atendimentos por médico
        df_atendimentos_medico = generate_atendimentos_por_medico_report(session)
        export_report_to_csv(df_atendimentos_medico, f'atendimentos_por_medico_report_{timestamp}.csv')
        export_report_to_pdf(df_atendimentos_medico, f'atendimentos_por_medico_report_{timestamp}.pdf')

        # Gerar gráfico de grupo de risco
        plot_grupo_risco_atendimentos(session, f'./reports/grupo_risco_atendimentos_{timestamp}.png')