# app/api/views.py
from flask import jsonify
from backend.database import get_session
from backend.models import Atendimento

def atendimentos_report():
    session = get_session()
    atendimentos = session.query(Atendimento).all()
    data = [{
        'Paciente': a.paciente.nome,
        'Clinica': a.clinica.nome,
        'Data': a.data_atendimento.isoformat()
    } for a in atendimentos]
    return jsonify(data)
