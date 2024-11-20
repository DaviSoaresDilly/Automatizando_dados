# application/reports/main.py

import sys
import os
import streamlit as st
from sqlalchemy.orm import Session

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from application.database import create_app, get_session
from descriptive_analysis import analise_distribuicao_doenca, analise_incidencia_bairros
from predictive_analysis import analise_clusterizacao_pacientes, analise_ocupacao_leitos
from statistical_analysis import analise_estatistica_atendimentos_medicos

# Inicializa o app Flask
app = create_app()

# Configurações do Streamlit
st.set_page_config(page_title="Análises de Dados de Saúde", layout="wide")
st.title("Análises de Dados de Saúde")

# Menu de Navegação
menu = ["Descritiva", "Preditiva", "Estatística"]
choice = st.sidebar.selectbox("Selecione o Tipo de Análise", menu)

# Navegação entre as páginas
if choice == "Descritiva":
    analise_distribuicao_doenca(app)
    analise_incidencia_bairros(app)
elif choice == "Preditiva":
    analise_ocupacao_leitos(app)
    analise_clusterizacao_pacientes(app)
elif choice == "Estatística":
    analise_estatistica_atendimentos_medicos(app)