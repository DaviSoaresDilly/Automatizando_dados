# app/analyze_occupacao_arima.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date, timedelta
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from application.models import Atendimento, Clinica

# Configurar conexão com o banco de dados
DATABASE_URL = "sqlite:///c:/Users/Davi/Documents/GitHub/Automatizando_dados/backend/instance/your_database.db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def extrair_dados_ocupacao(clinica_id: int, data_inicio: date, data_fim: date):
    """
    Extrai dados de ocupação de leitos para uma clínica específica dentro de um período de tempo.
    """
    atendimentos = (
        session.query(Atendimento)
        .filter(
            Atendimento.id_clinica == clinica_id,
            Atendimento.data_atendimento >= data_inicio,
            Atendimento.data_atendimento <= data_fim,
        )
        .all()
    )
    
    # Processar para DataFrame
    df = pd.DataFrame([
        {"data": atendimento.data_atendimento, "status": atendimento.status}
        for atendimento in atendimentos
    ])
    return df

def calcular_ocupacao_media(df, capacidade_leito: int):
    """
    Calcula a ocupação média diária de leitos.
    """
    ocupacao_diaria = df.groupby("data").size()
    ocupacao_media = ocupacao_diaria / capacidade_leito
    return ocupacao_media

def selecionar_melhor_arima(ocupacao_media):
    """
    Seleciona os melhores parâmetros ARIMA (p, d, q) com base no menor AIC.
    """
    melhor_aic = float("inf")
    melhor_parametros = None
    melhor_modelo = None

    for p in range(3):
        for d in range(2):
            for q in range(3):
                try:
                    modelo = ARIMA(ocupacao_media, order=(p, d, q)).fit()
                    aic = modelo.aic
                    if aic < melhor_aic:
                        melhor_aic = aic
                        melhor_parametros = (p, d, q)
                        melhor_modelo = modelo
                except:
                    continue  # Ignorar combinações que falhem

    return melhor_modelo, melhor_parametros

def prever_ocupacao_arima(clinica_id: int, dias_previstos: int = 30):
    """
    Previsão de ocupação de leitos usando ARIMA para uma clínica específica com ajuste automático de parâmetros.
    """
    data_fim = date.today()
    data_inicio = data_fim - timedelta(days=180)
    
    clinica = session.query(Clinica).filter(Clinica.id == clinica_id).first()
    if clinica is None:
        raise ValueError("Clínica não encontrada.")
    
    df_ocupacao = extrair_dados_ocupacao(clinica_id, data_inicio, data_fim)
    ocupacao_media = calcular_ocupacao_media(df_ocupacao, clinica.capacidade_leito)
    
    # Selecionar o melhor modelo ARIMA
    melhor_modelo, parametros = selecionar_melhor_arima(ocupacao_media)
    print(f"Melhores parâmetros ARIMA para a clínica {clinica_id}: {parametros}")
    
    # Fazer previsão com o modelo selecionado
    forecast = melhor_modelo.forecast(steps=dias_previstos)
    previsao_df = pd.DataFrame({"data": pd.date_range(start=data_fim, periods=dias_previstos, freq='D'),
                                "ocupacao_prevista": forecast})

    return previsao_df

if __name__ == "__main__":
    clinica_id = 1
    previsao_df = prever_ocupacao_arima(clinica_id)
    print(previsao_df)