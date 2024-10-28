# backend/models/atendimento_profissional.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from . import Base

class AtendimentoProfissional(Base):
    __tablename__ = 'atendimentos_profissionais'
    id = Column(Integer, primary_key=True)
    id_atendimento = Column(Integer, ForeignKey('atendimentos.id'), nullable=False)
    id_profissional = Column(Integer, ForeignKey('profissionais_saude.id'), nullable=False)
    funcao = Column(String(100), nullable=False)

    atendimento = relationship('Atendimento')
    profissional = relationship('ProfissionalSaude')
