# app/database/update_data.py
from sqlalchemy.orm import Session
from ..models import Atendimento, Paciente

def update_atendimento_status(session: Session, atendimento_id: int, new_status: str):
    """
    Atualiza o status de um atendimento.
    """
    atendimento = session.query(Atendimento).filter_by(id=atendimento_id).first()
    if atendimento:
        atendimento.status = new_status
        session.commit()
        return True
    return False

def update_paciente_info(session: Session, paciente_id: int, nome: str = None, idade: int = None):
    """
    Atualiza informações do paciente.
    """
    paciente = session.query(Paciente).filter_by(id=paciente_id).first()
    if paciente:
        if nome:
            paciente.nome = nome
        if idade:
            paciente.idade = idade
        session.commit()
        return True
    return False
