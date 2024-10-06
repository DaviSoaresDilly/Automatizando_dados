# app/models.py
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, Time
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Doenca(Base):
    __tablename__ = 'doencas'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    especialista = Column(String, nullable=False)
    sintomas = Column(String, nullable=False)
    gravidade = Column(String, nullable=False)
    requer_cirurgia = Column(Boolean, nullable=False)

    # Relacionamento com atendimentos
    atendimentos = relationship('Atendimento', back_populates='doenca')


class Bairro(Base):
    __tablename__ = 'bairros'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    pop_total = Column(Integer, nullable=False)
    infra_saude = Column(String)

    # Relacionamento com atendimentos
    atendimentos = relationship('Atendimento', back_populates='bairro')


class Paciente(Base):
    __tablename__ = 'pacientes'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    idade = Column(Integer, nullable=False)
    sexo = Column(String, nullable=False)
    endereco = Column(String)
    telefone = Column(String)

    # Relacionamento com atendimentos e prontuários
    atendimentos = relationship('Atendimento', back_populates='paciente')
    prontuarios = relationship('Prontuario', back_populates='paciente')


class Clinica(Base):
    __tablename__ = 'clinicas'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    tipo = Column(String, nullable=False)
    capacidade_diaria = Column(Integer)
    capacidade_leito = Column(Integer)
    endereco = Column(String)

    # Relacionamento com atendimentos
    atendimentos = relationship('Atendimento', back_populates='clinica')


class Medico(Base):
    __tablename__ = 'medicos'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    especialidade = Column(String, nullable=False)
    crm = Column(String, nullable=False)

    # Relacionamento com prontuários
    prontuarios = relationship('Prontuario', back_populates='medico')


class Atendimento(Base):
    __tablename__ = 'atendimentos'
    id = Column(Integer, primary_key=True)
    id_paciente = Column(Integer, ForeignKey('pacientes.id'), nullable=False)
    id_bairro = Column(Integer, ForeignKey('bairros.id'), nullable=False)
    id_doenca = Column(Integer, ForeignKey('doencas.id'), nullable=False)
    id_clinica = Column(Integer, ForeignKey('clinicas.id'), nullable=False)
    data_atendimento = Column(Date, nullable=False)
    status = Column(String, nullable=False)
    hora_atendimento = Column(Time, nullable=False)
    hora_conclusao = Column(Time, nullable=False)

    # Relacionamentos
    paciente = relationship('Paciente', back_populates='atendimentos')
    bairro = relationship('Bairro', back_populates='atendimentos')
    doenca = relationship('Doenca', back_populates='atendimentos')
    clinica = relationship('Clinica', back_populates='atendimentos')
    profissionais = relationship('AtendimentoProfissional', back_populates='atendimento')


class Prontuario(Base):
    __tablename__ = 'prontuarios'
    id = Column(Integer, primary_key=True)
    id_paciente = Column(Integer, ForeignKey('pacientes.id'), nullable=False)
    id_medico = Column(Integer, ForeignKey('medicos.id'), nullable=False)
    descricao = Column(String, nullable=False)
    data = Column(Date, nullable=False)
    hora = Column(Time, nullable=False)
    status_conclusao = Column(String, nullable=False)

    # Relacionamentos
    paciente = relationship('Paciente', back_populates='prontuarios')
    medico = relationship('Medico', back_populates='prontuarios')


class ProfissionalSaude(Base):
    __tablename__ = 'profissionais_saude'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    tipo = Column(String, nullable=False)  # Ex: 'Enfermeiro', 'Técnico de Enfermagem', 'Médico'
    crm = Column(String, nullable=True)  # Apenas médicos têm CRM, outros profissionais podem deixar vazio

    # Relacionamento com atendimentos
    atendimentos = relationship('AtendimentoProfissional', back_populates='profissional')


class AtendimentoProfissional(Base):
    __tablename__ = 'atendimento_profissional'
    id_atendimento = Column(Integer, ForeignKey('atendimentos.id'), primary_key=True)
    id_profissional = Column(Integer, ForeignKey('profissionais_saude.id'), primary_key=True)
    funcao = Column(String, nullable=False)  # Ex: 'Consulta', 'Acompanhamento', 'Cirurgia'

    # Relacionamentos
    atendimento = relationship('Atendimento', back_populates='profissionais')
    profissional = relationship('ProfissionalSaude', back_populates='atendimentos')
