# app/database.py
from flask_sqlalchemy import SQLAlchemy

from app.models import Atendimento

# Inicializando SQLAlchemy
db = SQLAlchemy()

# Inicializando o banco de dados no app Flask
def init_db(app):
    """Inicializa o banco de dados com o Flask app."""
    db.init_app(app)

# Função para obter a sessão do SQLAlchemy
def get_session():
    """Retorna a sessão atual."""
    return db.session

# Função de atualização de atendimento
def update_atendimento(session, atendimento_id, novos_dados):
    """
    Atualiza os dados de um atendimento existente.

    session: Sessão do banco de dados.
    atendimento_id: ID do atendimento a ser atualizado.
    novos_dados: Dicionário contendo os novos valores a serem aplicados.
    """
    atendimento = session.query(Atendimento).filter_by(id=atendimento_id).first()

    if atendimento is None:
        raise ValueError(f"Atendimento com ID {atendimento_id} não encontrado.")

    try:
        # Atualizando os atributos do atendimento
        for key, value in novos_dados.items():
            if hasattr(atendimento, key):
                setattr(atendimento, key, value)
            else:
                raise ValueError(f"O campo {key} não existe no modelo Atendimento.")

        # Confirma as mudanças no banco de dados
        session.commit()
    except Exception as e:
        session.rollback()  # Reverte a transação em caso de erro
        raise e  # Relevanta o erro para ser tratado mais acima

# Exemplo de uso em uma rota do Flask:
# @app.route('/update_atendimento/<int:atendimento_id>', methods=['POST'])
# def update(atendimento_id):
#     novos_dados = request.get_json()
#     session = get_session()
#     update_atendimento(session, atendimento_id, novos_dados)
#     return jsonify({"status": "sucesso"})
