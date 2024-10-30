# app/__init__.py
from fastapi import FastAPI
from .routers import pacientes, medicos, atendimentos, doencas

app = FastAPI()

# Incluindo rotas
app.include_router(pacientes.router)
app.include_router(medicos.router)
app.include_router(atendimentos.router)
app.include_router(doencas.router)
