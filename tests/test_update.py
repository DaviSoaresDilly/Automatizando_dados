# tests/test_update.py
import pytest
from app.database import create_app, get_session
from app.base_de_dados.update_data import update_atendimento_status, update_paciente_info
from app.models import Atendimento, Paciente

@pytest.fixture(scope='module')
def app():
    app = create_app()
    with app.app_context():
        yield app

@pytest.fixture
def session(app):
    session = get_session()
    # Inicialize o banco de dados e popule os dados necessários
    from app.models import Base
    Base.metadata.create_all(session.get_bind())
    # Popule os dados necessários para o teste
    yield session
    session.close()

def test_update_atendimento_status(session):
    atendimento = session.query(Atendimento).first()
    original_status = atendimento.status
    assert update_atendimento_status(session, atendimento.id, "Concluído") == True
    updated_atendimento = session.query(Atendimento).filter_by(id=atendimento.id).first()
    assert updated_atendimento.status == "Concluído"
    # Restaura o status original
    update_atendimento_status(session, atendimento.id, original_status)

def test_update_paciente_info(session):
    paciente = session.query(Paciente).first()
    original_name = paciente.nome
    original_age = paciente.idade
    assert update_paciente_info(session, paciente.id, nome="Teste Paciente", idade=30) == True
    updated_paciente = session.query(Paciente).filter_by(id=paciente.id).first()
    assert updated_paciente.nome == "Teste Paciente"
    assert updated_paciente.idade == 30
    # Restaura os dados originais
    update_paciente_info(session, paciente.id, nome=original_name, idade=original_age)