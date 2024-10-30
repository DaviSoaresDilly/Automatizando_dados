# app/main.py
from app import app
from fastapi import FastAPI
from app.routers import pacientes, medicos, atendimentos, agendamentos, doencas

app = FastAPI()

app.include_router(pacientes.router, prefix="/api/v1")
app.include_router(medicos.router, prefix="/api/v1")
app.include_router(atendimentos.router, prefix="/api/v1")
app.include_router(agendamentos.router, prefix="/api/v1")
app.include_router(doencas.router, prefix="/api/v1")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
