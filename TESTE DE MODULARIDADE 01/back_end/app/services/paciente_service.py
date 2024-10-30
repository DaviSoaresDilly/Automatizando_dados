from sqlalchemy.orm import Session
from ...models.paciente import Paciente

def criar_paciente(db: Session, nome: str, idade: int, sexo: str, endereco: str, telefone: str) -> Paciente:
    novo_paciente = Paciente(
        nome=nome,
        idade=idade,
        sexo=sexo,
        endereco=endereco,
        telefone=telefone
    )
    db.add(novo_paciente)
    db.commit()
    db.refresh(novo_paciente)
    return novo_paciente

def obter_paciente_por_id(db: Session, paciente_id: int) -> Paciente:
    return db.query(Paciente).filter(Paciente.id == paciente_id).first()

def listar_pacientes(db: Session) -> list:
    return db.query(Paciente).all()

def atualizar_paciente(db: Session, paciente_id: int, nome: str = None, idade: int = None, sexo: str = None, endereco: str = None, telefone: str = None) -> Paciente:
    paciente = db.query(Paciente).filter(Paciente.id == paciente_id).first()
    if not paciente:
        return None
    if nome:
        paciente.nome = nome
    if idade:
        paciente.idade = idade
    if sexo:
        paciente.sexo = sexo
    if endereco:
        paciente.endereco = endereco
    if telefone:
        paciente.telefone = telefone

    db.commit()
    db.refresh(paciente)
    return paciente

def deletar_paciente(db: Session, paciente_id: int) -> bool:
    paciente = db.query(Paciente).filter(Paciente.id == paciente_id).first()
    if not paciente:
        return False
    db.delete(paciente)
    db.commit()
    return True
