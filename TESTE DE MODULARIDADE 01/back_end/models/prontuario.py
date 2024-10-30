# backend/models/prontuario.py
from sqlalchemy import Column, Integer, String, Text, Date, Time, ForeignKey
from sqlalchemy.orm import relationship
from . import Base

class Prontuario(Base):
    __tablename__ = 'prontuarios'
    id = Column(Integer, primary_key=True)
    id_paciente = Column(Integer, ForeignKey('pacientes.id'), nullable=False)
    id_atendimento = Column(Integer, ForeignKey('atendimentos.id'), nullable=False)
    id_medico = Column(Integer, ForeignKey('medicos.id'), nullable=False)
    descricao = Column(Text, nullable=False)
    data = Column(Date, nullable=False)
    hora = Column(Time, nullable=False)
    status_conclusao = Column(String, nullable=False)

    paciente = relationship('Paciente', back_populates='prontuarios')
    atendimento = relationship('Atendimento')
    medico = relationship('Medico', back_populates='prontuarios')
