# app/__init__.py
from .models import Paciente, Doenca, Bairro, Clinica, Medico, Atendimento, Prontuario
from .database import get_session
