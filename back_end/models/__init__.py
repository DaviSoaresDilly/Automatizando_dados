# backend/models/__init__.py

from .doenca import Doenca
from .paciente import Paciente
from .atendimento import Atendimento
from .clinica import Clinica
from .medico import Medico
from .prontuario import Prontuario
from .bairro import Bairro
from .agendamento import Agendamento
from .atendimento_profissional import AtendimentoProfissional
from .atendimento_pulado import AtendimentoPulado

# Exporte o Base para facilitar a criação de tabelas
from sqlalchemy.orm import declarative_base
Base = declarative_base()
