# back_end/app/routers/pacientes.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.services.paciente_service import (
    criar_paciente,
    obter_paciente_por_id,
    listar_pacientes,
    atualizar_paciente,
    deletar_paciente,
)
from base_de_dados.database import get_db

router = APIRouter()

@router.post("/pacientes", status_code=status.HTTP_201_CREATED)
def criar_paciente_endpoint(nome: str, idade: int, sexo: str, endereco: str, telefone: str, db: Session = Depends(get_db)):
    return criar_paciente(db, nome, idade, sexo, endereco, telefone)

@router.get("/pacientes/{paciente_id}")
def obter_paciente(paciente_id: int, db: Session = Depends(get_db)):
    paciente = obter_paciente_por_id(db, paciente_id)
    if paciente is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paciente não encontrado")
    return paciente

@router.get("/pacientes")
def listar_pacientes_endpoint(db: Session = Depends(get_db)):
    return listar_pacientes(db)

@router.put("/pacientes/{paciente_id}")
def atualizar_paciente_endpoint(paciente_id: int, nome: str = None, idade: int = None, sexo: str = None, endereco: str = None, telefone: str = None, db: Session = Depends(get_db)):
    paciente = atualizar_paciente(db, paciente_id, nome, idade, sexo, endereco, telefone)
    if paciente is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paciente não encontrado")
    return paciente

@router.delete("/pacientes/{paciente_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_paciente_endpoint(paciente_id: int, db: Session = Depends(get_db)):
    if not deletar_paciente(db, paciente_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paciente não encontrado")
