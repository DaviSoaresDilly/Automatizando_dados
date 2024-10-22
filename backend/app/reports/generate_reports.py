# app/reports/generate_reports.py
import pandas as pd
from sqlalchemy.orm import Session
from ..models import Atendimento, Clinica

import pandas as pd
from sqlalchemy.orm import Session
from ..models import Atendimento, Clinica, Paciente, Doenca, Bairro

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
    analise_por_faixa = df.groupby(['Faixa Etária', 'Sexo', 'Doenca']).size().reset_index(name='Incidências')

    return analise_por_faixa

# Funções de exportação (CSV e PDF) para qualquer DataFrame gerado
def export_report_to_csv(df: pd.DataFrame, filename: str):
    df.to_csv(filename, index=False)

def export_report_to_pdf(df: pd.DataFrame, filename: str):
    from fpdf import FPDF

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Relatório", ln=True, align='C')

    for index, row in df.iterrows():
        linha = ' | '.join([f"{col}: {str(row[col])}" for col in df.columns])
        pdf.cell(200, 10, txt=linha, ln=True)

    pdf.output(filename)
