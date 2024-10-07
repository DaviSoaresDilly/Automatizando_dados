# app/reports/generate_reports.py
import pandas as pd
from sqlalchemy.orm import Session
from backend.models import Atendimento, Clinica

def generate_atendimentos_report(session: Session) -> pd.DataFrame:
    """
    Gera um relatório com a contagem de atendimentos por clínica.
    """
    atendimentos = session.query(Atendimento).all()
    clinicas = session.query(Clinica).all()

    data = []

    for clinica in clinicas:
        atendimentos_por_clinica = session.query(Atendimento).filter_by(id_clinica=clinica.id).count()
        data.append({
            'Clinica': clinica.nome,
            'Total Atendimentos': atendimentos_por_clinica
        })

    df = pd.DataFrame(data)
    return df

def generate_atendimentos_report_paginated(session, page: int = 1, per_page: int = 50) -> pd.DataFrame:
    """
    Gera um relatório com a contagem de atendimentos por clínica com paginação.
    """
    offset = (page - 1) * per_page
    atendimentos = session.query(Atendimento).offset(offset).limit(per_page).all()

    data = []
    for atendimento in atendimentos:
        data.append({
            'Clinica': atendimento.clinica.nome,
            'Paciente': atendimento.paciente.nome,
            'Status': atendimento.status,
        })

    df = pd.DataFrame(data)
    return df

def export_report_to_csv(df: pd.DataFrame, filename: str):
    """
    Exporta o relatório para um arquivo CSV.
    """
    df.to_csv(filename, index=False)

def export_report_to_pdf(df: pd.DataFrame, filename: str):
    """
    Exporta o relatório para um arquivo PDF.
    """
    from fpdf import FPDF

    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Relatório de Atendimentos por Clínica", ln=True, align='C')

    # Inserir os dados do dataframe no PDF
    for index, row in df.iterrows():
        pdf.cell(200, 10, txt=f"{row['Clinica']}: {row['Total Atendimentos']} atendimentos", ln=True)

    pdf.output(filename)

