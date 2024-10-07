# tests/test_reports.py
import pytest
from app.database import get_session
from app.reports.generate_reports import generate_atendimentos_report, export_report_to_csv, export_report_to_pdf
import os

@pytest.fixture
def session():
    session = get_session()
    yield session
    session.close()

def test_generate_report(session):
    df = generate_atendimentos_report(session)
    assert not df.empty
    assert 'Clinica' in df.columns
    assert 'Total Atendimentos' in df.columns

def test_export_report_to_csv(session):
    df = generate_atendimentos_report(session)
    filename = "atendimentos_report.csv"
    export_report_to_csv(df, filename)
    assert os.path.exists(filename)
    os.remove(filename)

def test_export_report_to_pdf(session):
    df = generate_atendimentos_report(session)
    filename = "atendimentos_report.pdf"
    export_report_to_pdf(df, filename)
    assert os.path.exists(filename)
    os.remove(filename)
