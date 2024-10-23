# tests/test_database.py
import pytest
from app.database import create_app, get_session
from app.populate import populate_data
from app.generate_atendimentos import generate_atendimentos
from app.models import Atendimento, Prontuario, Paciente, Clinica

@pytest.fixture(scope='module')
def app():
    app = create_app()
    with app.app_context():
        yield app

@pytest.fixture
def session(app):
    session = get_session()
    yield session
    session.close()

def test_populate_data(session):
    populate_data(session)
    # Verifica se os dados de pacientes e clínicas foram populados corretamente
    assert session.query(Paciente).count() > 0
    assert session.query(Clinica).count() > 0

def test_generate_atendimentos(session):
    generate_atendimentos(session, 100)
    # Verifica se os atendimentos e prontuários foram criados
    assert session.query(Atendimento).count() > 0
    assert session.query(Prontuario).count() > 0

def test_paciente_dados(session):
    paciente = session.query(Paciente).first()
    # Verifica se os dados de paciente estão corretos
    assert paciente.nome is not None
    assert 0 <= paciente.idade <= 100

def test_atendimento_relacionamento(session):
    atendimento = session.query(Atendimento).first()
    # Verifica se o atendimento está corretamente relacionado a paciente e clínica
    assert atendimento.paciente is not None
    assert atendimento.clinica is not None

def test_no_atendimento_duplicado(session):
    generate_atendimentos(session, 100)
    # Verifica que não há atendimentos duplicados
    atendimentos = session.query(Atendimento).all()
    unique_ids = {atendimento.id for atendimento in atendimentos}
    assert len(atendimentos) == len(unique_ids), "Existem atendimentos duplicados"

def test_performance_generate_atendimentos(session):
    import time
    start_time = time.time()
    generate_atendimentos(session, 1000)
    end_time = time.time()
    # Verifica se a geração de 1000 atendimentos demora menos de 60 segundos
    assert (end_time - start_time) < 60, "A geração de atendimentos foi muito lenta"
