# app/reports/visualize.py
import matplotlib.pyplot as plt
import pandas as pd

def plot_atendimentos_por_clinica(df: pd.DataFrame, save_path: str = None):
    """
    Gera um gráfico de barras com a quantidade de atendimentos por clínica.
    """
    df = df.sort_values(by='Total Atendimentos', ascending=False)
    plt.figure(figsize=(10, 6))
    plt.barh(df['Clinica'], df['Total Atendimentos'], color='teal')
    plt.xlabel("Número de Atendimentos")
    plt.ylabel("Clínica")
    plt.title("Atendimentos por Clínica")
    if save_path:
        plt.savefig(save_path)
    plt.show()

def plot_grupo_risco_atendimentos(session, save_path: str = None):
    """
    Gera um gráfico de pizza com a proporção de atendimentos de pacientes em grupo de risco.
    """
    from app.models import Paciente, Atendimento

    atendimentos = session.query(Atendimento).all()
    total_grupo_risco = sum(1 for a in atendimentos if a.paciente.idade >= 60 or 'Gestante' in a.paciente.sexo)
    total_outros = len(atendimentos) - total_grupo_risco

    labels = ['Grupo de Risco', 'Outros']
    sizes = [total_grupo_risco, total_outros]
    colors = ['#ff9999','#66b3ff']
    explode = (0.1, 0)

    plt.figure(figsize=(7, 7))
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    plt.title("Proporção de Atendimentos para Grupo de Risco")
    if save_path:
        plt.savefig(save_path)
    plt.show()