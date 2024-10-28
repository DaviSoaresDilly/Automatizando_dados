# backend/models/doenca.py
from sqlalchemy import Column, Integer, String, Boolean, Text
from sqlalchemy.orm import relationship
from . import Base
import json

class Doenca(Base):
    __tablename__ = 'doencas'
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    especialista = Column(String(100), nullable=False)
    sintomas = Column(Text, nullable=False)
    requer_cirurgia = Column(Boolean, nullable=False)
    gravidade = Column(String(20), nullable=False)

    atendimentos = relationship('Atendimento', back_populates='doenca')

    def __init__(self, nome, especialista, sintomas, requer_cirurgia, gravidade):
        self.nome = nome
        self.especialista = especialista
        self.sintomas = json.dumps(sintomas)
        self.requer_cirurgia = requer_cirurgia
        self.gravidade = gravidade
