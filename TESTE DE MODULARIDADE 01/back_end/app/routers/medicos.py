# back_end/app/routers/medicos.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.services.medico_service import (
    criar_medico,
    obter_medico_por_id,
    listar_medicos,
    atualizar_medico,
    deletar_medico,
)
from base_de_dados.database import get_db

router = APIRouter()

@router.post("/medicos", status_code=status.HTTP_201_CREATED)
def criar_medico_endpoint(nome: str, especialidade: str, crm: str, id_clinica: int, db: Session = Depends(get_db)):
    return criar_medico(db, nome, especialidade, crm, id_clinica)

@router.get("/medicos/{medico_id}")
def obter_medico(medico_id: int, db: Session = Depends(get_db)):
    medico = obter_medico_por_id(db, medico_id)
    if medico is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Médico não encontrado")
    return medico

@router.get("/medicos")
def listar_medicos_endpoint(db: Session = Depends(get_db)):
    return listar_medicos(db)

@router.put("/medicos/{medico_id}")
def atualizar_medico_endpoint(medico_id: int, nome: str = None, especialidade: str = None, crm: str = None, id_clinica: int = None, db: Session = Depends(get_db)):
    medico = atualizar_medico(db, medico_id, nome, especialidade, crm, id_clinica)
    if medico is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Médico não encontrado")
    return medico

@router.delete("/medicos/{medico_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_medico_endpoint(medico_id: int, db: Session = Depends(get_db)):
    if not deletar_medico(db, medico_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Médico não encontrado")
