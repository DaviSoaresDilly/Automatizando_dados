# app/validators.py
def validar_dados_atendimento(data):
    if 'Paciente' not in data or 'Clinica' not in data or 'Data' not in data:
        raise ValueError("Dados de atendimento inválidos")
