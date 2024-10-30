from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.services.atendimento_service import (
    criar_atendimento,
    obter_atendimento_por_id,
    listar_atendimentos,
    atualizar_atendimento,
    deletar_atendimento,
)
from base_de_dados.database import get_db

router = APIRouter()

@router.post("/atendimentos", status_code=status.HTTP_201_CREATED)
def criar_atendimento_endpoint(...):
    # Similar ao exemplo anterior, crie as rotas CRUD para Atendimento
