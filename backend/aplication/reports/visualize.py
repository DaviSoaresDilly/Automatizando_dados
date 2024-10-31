# app/reports/visualize.py

import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def ensure_output_dir(output_dir: str):
    """
    Garante que o diretório de saída exista.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

def plot_ocupacao_historico_previsao(df_historico: pd.DataFrame, df_previsao: pd.DataFrame, clinica_nome: str):
    """
    Gera o gráfico da ocupação histórica e previsão futura de leitos para uma clínica.
    """
    plt.figure(figsize=(12, 6))
    plt.plot(df_historico["data"], df_historico["ocupacao"], label="Histórico de Ocupação", color="blue", marker="o")
    plt.plot(df_previsao["data"], df_previsao["ocupacao_prevista"], label="Previsão de Ocupação", color="red", linestyle="--", marker="x")
    
    plt.title(f"Previsão de Ocupação de Leitos - {clinica_nome}")
    plt.xlabel("Data")
    plt.ylabel("Taxa de Ocupação (%)")
    plt.legend(loc="upper left")
    plt.grid(True)
    
    output_dir = "./reports"
    ensure_output_dir(output_dir)
    output_path = os.path.join(output_dir, f"ocupacao_previsao_{clinica_nome.replace(' ', '_')}.png")
    plt.savefig(output_path)
    plt.show()
    print(f"Gráfico salvo em: {output_path}")

def plot_distribution_by_age_gender(df_distribuicao: pd.DataFrame):
    """
    Gera um gráfico de barras para mostrar a distribuição de doenças por faixa etária e sexo.
    """
    plt.figure(figsize=(12, 8))
    sns.barplot(data=df_distribuicao, x='Faixa Etária', y='Incidências', hue='Sexo', errorbar=None)  # Atualizado para errorbar=None
    
    plt.title("Distribuição de Doenças por Faixa Etária e Sexo")
    plt.xlabel("Faixa Etária")
    plt.ylabel("Número de Incidências")
    plt.legend(title="Sexo")
    plt.xticks(rotation=45)
    plt.grid(True, axis='y', linestyle='--', linewidth=0.7)
    plt.tight_layout()

    output_dir = "./reports"
    ensure_output_dir(output_dir)
    output_path = os.path.join(output_dir, "distribuicao_faixa_etaria_sexo.png")
    plt.savefig(output_path)
    plt.show()
    print(f"Gráfico salvo em: {output_path}")

def plot_doenca_por_bairro(df_doenca_bairro: pd.DataFrame):
    """
    Gera e salva um gráfico de barras da quantidade de doenças por bairro.
    """
    plt.figure(figsize=(14, 10))
    
    sns.barplot(data=df_doenca_bairro, x='Doença', y='Quantidade', hue='Bairro', errorbar=None)  # Atualizado para errorbar=None
    
    plt.title('Quantidade de Doenças por Bairro')
    plt.xlabel('Doença')
    plt.ylabel('Quantidade de Incidências')
    plt.legend(title='Bairro')
    plt.xticks(rotation=45, ha='right')
    plt.grid(True, axis='y', linestyle='--', linewidth=0.7)
    plt.tight_layout()
    
    output_dir = "./reports"
    ensure_output_dir(output_dir)
    output_path = os.path.join(output_dir, "doenca_por_bairro.png")
    plt.savefig(output_path)  # Salvar o gráfico antes de exibir
    plt.show()
    print(f"Gráfico salvo em: {output_path}")
