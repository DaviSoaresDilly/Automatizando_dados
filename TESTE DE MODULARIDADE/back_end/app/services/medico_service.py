from sqlalchemy.orm import Session
from ...models.medico import Medico

def criar_medico(db: Session, nome: str, especialidade: str, crm: str, id_clinica: int) -> Medico:
    novo_medico = Medico(
        nome=nome,
        especialidade=especialidade,
        crm=crm,
        id_clinica=id_clinica
    )
    db.add(novo_medico)
    db.commit()
    db.refresh(novo_medico)
    return novo_medico

def obter_medico_por_id(db: Session, medico_id: int) -> Medico:
    return db.query(Medico).filter(Medico.id == medico_id).first()

def listar_medicos(db: Session) -> list:
    return db.query(Medico).all()

def atualizar_medico(db: Session, medico_id: int, nome: str = None, especialidade: str = None, crm: str = None, id_clinica: int = None) -> Medico:
    medico = db.query(Medico).filter(Medico.id == medico_id).first()
    if not medico:
        return None
    if nome:
        medico.nome = nome
    if especialidade:
        medico.especialidade = especialidade
    if crm:
        medico.crm = crm
    if id_clinica:
        medico.id_clinica = id_clinica

    db.commit()
    db.refresh(medico)
    return medico

def deletar_medico(db: Session, medico_id: int) -> bool:
    medico = db.query(Medico).filter(Medico.id == medico_id).first()
    if not medico:
        return False
    db.delete(medico)
    db.commit()
    return True
