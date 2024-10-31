# backend/app/api/routes.py

from flask import Blueprint, jsonify

# Blueprint para organizar as rotas da API
api_blueprint = Blueprint('api', __name__)

# Exemplo de rota para teste
@api_blueprint.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "API funcionando corretamente"})
