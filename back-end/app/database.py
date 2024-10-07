# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy

from .models import Atendimento

# Banco de dados SQLite local
DATABASE_URL = "sqlite:///meu_banco.db"

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_session():
    return SessionLocal()

# Nova função de atualização de dados
def update_atendimento(session, atendimento_id, novos_dados):
    atendimento = session.query(Atendimento).filter(Atendimento.id == atendimento_id).first()
    if atendimento:
        for key, value in novos_dados.items():
            setattr(atendimento, key, value)
        session.commit()
