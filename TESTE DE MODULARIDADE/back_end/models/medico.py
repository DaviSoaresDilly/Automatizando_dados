# backend/models/medico.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from . import Base

class Medico(Base):
    __tablename__ = 'medicos'
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    especialidade = Column(String(100), nullable=False)
    crm = Column(String(20), nullable=False)
    id_clinica = Column(Integer, ForeignKey('clinicas.id'), nullable=False)

    prontuarios = relationship('Prontuario', back_populates='medico')
    clinica = relationship('Clinica', back_populates='medicos')
    atendimentos = relationship('Atendimento', back_populates='medico')
