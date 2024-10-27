# app/models.py
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, Text, Time
from sqlalchemy.orm import relationship, declarative_base
import json

Base = declarative_base()

class Doenca(Base):
    __tablename__ = 'doencas'
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    especialista = Column(String(100), nullable=False)
    sintomas = Column(Text, nullable=False)
    requer_cirurgia = Column(Boolean, nullable=False)
    gravidade = Column(String(20), nullable=False)

    # Relacionamento com atendimentos
    atendimentos = relationship('Atendimento', back_populates='doenca')

    def __init__(self, nome, especialista, sintomas, requer_cirurgia, gravidade):
        self.nome = nome
        self.especialista = especialista
        self.sintomas = json.dumps(sintomas)  # Armazenar sintomas como string JSON
        self.requer_cirurgia = requer_cirurgia
        self.gravidade = gravidade

class Bairro(Base):
    __tablename__ = 'bairros'
    id = Column(Integer, primary_key=True)
    nome = Column(String(50), unique=True, nullable=False)
    pop_total = Column(Integer, nullable=False)
    infra_saude = Column(Text)

    # Relacionamento com atendimentos
    atendimentos = relationship("Atendimento", back_populates="bairro")

class Paciente(Base):
    __tablename__ = 'pacientes'
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    idade = Column(Integer, nullable=False)
    sexo = Column(String(1), nullable=False)
    endereco = Column(Text, nullable=False)
    telefone = Column(String(20), nullable=False)

    # Relacionamento com atendimentos
    atendimentos = relationship('Atendimento', back_populates='paciente')
    prontuarios = relationship('Prontuario', back_populates='paciente')

class Clinica(Base):
    __tablename__ = 'clinicas'
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    tipo = Column(String(20), nullable=False)
    capacidade_diaria = Column(Integer, nullable=False)
    capacidade_leito = Column(Integer, nullable=False)
    endereco = Column(Text, nullable=False)

    # Relacionamento com atendimentos
    atendimentos = relationship('Atendimento', back_populates='clinica')
    medicos = relationship('Medico', back_populates='clinica')

class Medico(Base):
    __tablename__ = 'medicos'
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    especialidade = Column(String(100), nullable=False)
    crm = Column(String(20), nullable=False)
    id_clinica = Column(Integer, ForeignKey('clinicas.id'), nullable=False)

    # Relacionamento com prontuarios
    prontuarios = relationship('Prontuario', back_populates='medico')
    clinica = relationship('Clinica', back_populates='medicos')

    # Relacionamento com atendimentos
    atendimentos = relationship('Atendimento', back_populates='medico')

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

    # Relacionamentos
    paciente = relationship('Paciente', back_populates='atendimentos')
    bairro = relationship('Bairro', back_populates='atendimentos')
    doenca = relationship('Doenca', back_populates='atendimentos')
    clinica = relationship('Clinica', back_populates='atendimentos')
    medico = relationship('Medico', back_populates='atendimentos')

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

    # Relacionamentos
    paciente = relationship('Paciente', back_populates='prontuarios')
    atendimento = relationship('Atendimento')
    medico = relationship('Medico', back_populates='prontuarios')

class ProfissionalSaude(Base):
    __tablename__ = 'profissionais_saude'
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    tipo = Column(String(50), nullable=False)

class AtendimentoProfissional(Base):
    __tablename__ = 'atendimentos_profissionais'
    id = Column(Integer, primary_key=True)
    id_atendimento = Column(Integer, ForeignKey('atendimentos.id'), nullable=False)
    id_profissional = Column(Integer, ForeignKey('profissionais_saude.id'), nullable=False)
    funcao = Column(String(100), nullable=False)

    # Relacionamentos
    atendimento = relationship('Atendimento')
    profissional = relationship('ProfissionalSaude')

class AtendimentoPulado(Base):
    __tablename__ = 'atendimentos_pulados'
    id = Column(Integer, primary_key=True)
    id_paciente = Column(Integer, ForeignKey('pacientes.id'), nullable=False)
    id_bairro = Column(Integer, ForeignKey('bairros.id'), nullable=False)
    id_doenca = Column(Integer, ForeignKey('doencas.id'), nullable=False)
    motivo = Column(String, nullable=False)
    data_tentativa = Column(Date, nullable=False)

class Agendamento(Base):
    __tablename__ = 'agendamentos'
    id = Column(Integer, primary_key=True)
    paciente_id = Column(Integer, ForeignKey('pacientes.id'), nullable=False)
    medico_id = Column(Integer, ForeignKey('medicos.id'), nullable=False)
    data_hora = Column(Date, nullable=False)
    status_conclusao = Column(String, nullable=False)

    # Relacionamentos
    paciente = relationship('Paciente')
    medico = relationship('Medico')