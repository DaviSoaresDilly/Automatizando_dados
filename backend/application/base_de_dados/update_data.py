# app/base_de_dados/update_data.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from ..models import Atendimento, Paciente

def update_atendimento_status(session: Session, atendimento_id: int, new_status: str):
    """
    Atualiza o status de um atendimento.
    """
    try:
        atendimento = session.get(Atendimento, atendimento_id)  # Uso de get() para chave primária
        if atendimento:
            atendimento.status = new_status
            session.commit()
            return True  # Retorna True após a atualização bem-sucedida
        return {"error": f"Atendimento com ID {atendimento_id} não encontrado."}
    except SQLAlchemyError as e:
        session.rollback()  # Reverte a transação em caso de erro
        return {"error": str(e)}

def update_paciente_info(session: Session, paciente_id: int, nome: str = None, idade: int = None):
    """
    Atualiza informações do paciente.
    """
    try:
        paciente = session.get(Paciente, paciente_id)  # Uso de get() para chave primária
        if paciente:
            if nome:
                paciente.nome = nome
            if idade is not None:  # Verifica se idade não é None
                paciente.idade = idade
            session.commit()
            return True  # Retorna True após a atualização bem-sucedida
        return {"error": f"Paciente com ID {paciente_id} não encontrado."}
    except SQLAlchemyError as e:
        session.rollback()  # Reverte a transação em caso de erro
        return {"error": str(e)}