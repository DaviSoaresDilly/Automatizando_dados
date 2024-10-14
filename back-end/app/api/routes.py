# app/api/routes.py
from flask import Flask
from .views import atendimentos_report

app = Flask(__name__)

# Define rota para obter os atendimentos em formato JSON
@app.route('/api/atendimentos', methods=['GET'])
def get_atendimentos():
    return atendimentos_report()
