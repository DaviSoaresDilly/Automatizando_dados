# backend/models/atendimento_pulado.py
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from . import Base

class AtendimentoPulado(Base):
    __tablename__ = 'atendimentos_pulados'
    id = Column(Integer, primary_key=True)
    id_paciente = Column(Integer, ForeignKey('pacientes.id'), nullable=False)
    id_bairro = Column(Integer, ForeignKey('bairros.id'), nullable=False)
    id_doenca = Column(Integer, ForeignKey('doencas.id'), nullable=False)
    motivo = Column(String, nullable=False)
    data_tentativa = Column(Date, nullable=False)
