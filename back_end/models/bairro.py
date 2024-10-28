# backend/models/bairro.py
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from . import Base

class Bairro(Base):
    __tablename__ = 'bairros'
    id = Column(Integer, primary_key=True)
    nome = Column(String(50), unique=True, nullable=False)
    pop_total = Column(Integer, nullable=False)
    infra_saude = Column(Text)

    atendimentos = relationship("Atendimento", back_populates="bairro")
