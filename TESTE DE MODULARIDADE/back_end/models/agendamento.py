# backend/models/agendamento.py
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from . import Base

class Agendamento(Base):
    __tablename__ = 'agendamentos'
    id = Column(Integer, primary_key=True)
    paciente_id = Column(Integer, ForeignKey('pacientes.id'), nullable=False)
    medico_id = Column(Integer, ForeignKey('medicos.id'), nullable=False)
    data_hora = Column(Date, nullable=False)
    status_conclusao = Column(String, nullable=False)

    paciente = relationship('Paciente')
    medico = relationship('Medico')
