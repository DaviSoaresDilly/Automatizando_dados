# app/validators.py

def validar_dados_atendimento(data):
    """
    Valida os dados do atendimento, verificando a presença e consistência das informações.
    """
    campos_obrigatorios = ['Paciente', 'Clinica', 'Data', 'Doenca', 'Medico', 'HoraAtendimento']

    # Verificar se todos os campos obrigatórios estão presentes
    for campo in campos_obrigatorios:
        if campo not in data:
            raise ValueError(f"Campo obrigatório '{campo}' não está presente nos dados.")

    # Verificar se a data de atendimento é válida
    if not isinstance(data['Data'], str):  # Exemplo de verificação simples
        raise ValueError("O campo 'Data' deve ser uma string no formato YYYY-MM-DD.")

    # Verificar se o paciente é maior de idade
    if data.get('Paciente').get('idade') < 0:
        raise ValueError("A idade do paciente não pode ser negativa.")

    # Verificar se a clínica tem capacidade
    if data.get('Clinica').get('capacidade_diaria') <= 0:
        raise ValueError(f"A clínica {data.get('Clinica').get('nome')} não tem capacidade para atendimentos.")

    # Verificar se a doença requer cirurgia e se a clínica tem leitos
    if data.get('Doenca').get('requer_cirurgia') and data.get('Clinica').get('capacidade_leito') <= 0:
        raise ValueError(f"A clínica {data.get('Clinica').get('nome')} não possui leitos para cirurgias.")

    # Verificar se a hora de atendimento é válida (opcional, baseado em regra de negócio)
    if not isinstance(data['HoraAtendimento'], str):  # Exemplo de verificação
        raise ValueError("O campo 'HoraAtendimento' deve ser uma string no formato HH:MM:SS.")

    # Validação de status
    status_validos = ['Concluído', 'Em andamento', 'Cancelado', 'Aguardando']
    if data.get('status') not in status_validos:
        raise ValueError(f"Status '{data.get('status')}' é inválido. Valores permitidos: {status_validos}")

    # Validação de médico especializado para doenças graves
    if data.get('Doenca').get('gravidade') in ['Grave', 'Muito Grave']:
        if data.get('Medico').get('especialidade') != data.get('Doenca').get('especialista'):
            raise ValueError(f"O médico selecionado não é especializado para tratar a doença '{data.get('Doenca').get('nome')}'.")

    # Se todas as validações passarem
    return True
