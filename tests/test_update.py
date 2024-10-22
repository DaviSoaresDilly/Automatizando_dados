# tests/test_update.py
import pytest
from app.database import get_session
from app.base_de_dados.update_data import update_atendimento_status, update_paciente_info
from app.models import Atendimento, Paciente

@pytest.fixture
def session():
    session = get_session()
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
