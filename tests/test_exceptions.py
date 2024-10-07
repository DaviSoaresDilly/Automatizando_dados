# tests/test_exceptions.py
import pytest
from sqlalchemy.exc import IntegrityError
from backend.database import get_session
from backend.models import Atendimento, Paciente

@pytest.fixture
def session():
    session = get_session()
    yield session
    session.close()

def test_integrity_error(session):
    # Tenta criar um atendimento com dados inválidos para testar a integridade
    invalid_atendimento = Atendimento(id_paciente=9999, id_bairro=1, id_doenca=1, id_clinica=1)
    
    with pytest.raises(IntegrityError):
        session.add(invalid_atendimento)
        session.commit()

def test_database_disconnection(session):
    # Simula a desconexão do banco de dados
    session.connection().close()

    with pytest.raises(Exception):
        session.query(Paciente).first()  # Tenta acessar o banco de dados após desconexão

def test_invalid_data_insertion(session):
    # Insere dados inválidos e verifica se o sistema lida corretamente com o erro
    paciente_invalido = Paciente(nome=None, idade=-5, sexo='')

    with pytest.raises(Exception) as e_info:
        session.add(paciente_invalido)
        session.commit()

    # Verifica a violação da restrição NOT NULL para o campo nome
    assert "NOT NULL constraint failed" in str(e_info.value), "Erro não esperado: violação da restrição NOT NULL"

    # Opcional: se você tiver uma CHECK constraint para a idade ou outro campo, adicione outra verificação
    # assert "CHECK constraint failed" in str(e_info.value), "Erro não esperado: violação da restrição CHECK"
