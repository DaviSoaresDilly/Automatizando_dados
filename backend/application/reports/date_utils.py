# application/reports/date_utils.py

from datetime import date, datetime
import pandas as pd

def calculate_date_range(period: str, ano: int, mes: int = None, trimestre: str = None):
    """
    Calcula a data de início com base no período selecionado.
    """
    if period == "Mensal" and mes:
        start_date = date(ano, mes, 1)
        end_date = (datetime(ano, mes, 1) + pd.DateOffset(months=1) - pd.DateOffset(days=1)).date()
    elif period == "Trimestral" and trimestre:
        if trimestre == "1º Trimestre":
            start_date = date(ano, 1, 1)
        elif trimestre == "2º Trimestre":
            start_date = date(ano, 4, 1)
        elif trimestre == "3º Trimestre":
            start_date = date(ano, 7, 1)
        elif trimestre == "4º Trimestre":
            start_date = date(ano, 10, 1)
        end_date = (datetime(ano, start_date.month, 1) + pd.DateOffset(months=3) - pd.DateOffset(days=1)).date()
    elif period == "Anual":
        start_date = date(ano, 1, 1)
        end_date = date(ano, 12, 31)
    else:
        raise ValueError("Período inválido")
    
    # Log para verificar a data de início calculada
    print(f"Data de início calculada para o período '{period}': {start_date}")
    return start_date, end_date

def get_period_label(period, start_date, end_date):
    if period == "Mensal":
        return start_date.strftime("%B de %Y")
    elif period == "Trimestral":
        return f"{start_date.strftime('%B')} a {end_date.strftime('%B de %Y')}"
    elif period == "Anual":
        return start_date.strftime("%Y")
    return ""