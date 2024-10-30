# backend/models/paciente.py
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from . import Base

class Paciente(Base):
    __tablename__ = 'pacientes'
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    idade = Column(Integer, nullable=False)
    sexo = Column(String(1), nullable=False)
    endereco = Column(Text, nullable=False)
    telefone = Column(String(20), nullable=False)

    atendimentos = relationship('Atendimento', back_populates='paciente')
    prontuarios = relationship('Prontuario', back_populates='paciente')
