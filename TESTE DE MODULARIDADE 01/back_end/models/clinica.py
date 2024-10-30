# backend/models/clinica.py
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from . import Base

class Clinica(Base):
    __tablename__ = 'clinicas'
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    tipo = Column(String(20), nullable=False)
    capacidade_diaria = Column(Integer, nullable=False)
    capacidade_leito = Column(Integer, nullable=False)
    endereco = Column(Text, nullable=False)

    atendimentos = relationship('Atendimento', back_populates='clinica')
    medicos = relationship('Medico', back_populates='clinica')
