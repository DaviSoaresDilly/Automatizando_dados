# backend/models/atendimento.py
from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey
from sqlalchemy.orm import relationship
from . import Base

class Atendimento(Base):
    __tablename__ = 'atendimentos'
    id = Column(Integer, primary_key=True)
    id_paciente = Column(Integer, ForeignKey('pacientes.id'), nullable=False)
    id_bairro = Column(Integer, ForeignKey('bairros.id'), nullable=False)
    id_doenca = Column(Integer, ForeignKey('doencas.id'), nullable=False)
    id_clinica = Column(Integer, ForeignKey('clinicas.id'), nullable=False)
    id_medico = Column(Integer, ForeignKey('medicos.id'), nullable=False)
    data_atendimento = Column(Date, nullable=False)
    status = Column(String, nullable=False)
    hora_atendimento = Column(Time, nullable=False)
    hora_conclusao = Column(Time, nullable=False)

    paciente = relationship('Paciente', back_populates='atendimentos')
    bairro = relationship('Bairro', back_populates='atendimentos')
    doenca = relationship('Doenca', back_populates='atendimentos')
    clinica = relationship('Clinica', back_populates='atendimentos')
    medico = relationship('Medico', back_populates='atendimentos')
