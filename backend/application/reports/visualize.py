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


def plot_ocupacao_historico_previsao(df_historico, df_previsao, clinica_nome, fig, ax):
    ax.plot(
        df_historico["data"],
        df_historico["Ocupação Histórica"],
        label="Histórico de Ocupação",
        color="blue",
        marker="o",
    )
    ax.plot(
        df_previsao["data"],
        df_previsao["Ocupação Prevista"],
        label="Previsão de Ocupação",
        color="red",
        linestyle="--",
        marker="x",
    )

    ax.set_title(f"Previsão de Ocupação de Leitos - {clinica_nome}")
    ax.set_xlabel("Data")
    ax.set_ylabel("Taxa de Ocupação (%)")
    ax.legend(loc="upper left")
    ax.grid(True)


def plot_distribution_by_age_gender(df_distribuicao, fig, ax):
    sns.barplot(
        data=df_distribuicao,
        x="Faixa Etária",
        y="Incidências",
        hue="Sexo",
        errorbar=None,
        ax=ax,
    )  # Usar `errorbar=None` ao invés de `ci=None`

    ax.set_title("Distribuição de Doenças por Faixa Etária e Sexo")
    ax.set_xlabel("Faixa Etária")
    ax.set_ylabel("Número de Incidências")
    ax.legend(title="Sexo")
    ax.grid(True, axis="y", linestyle="--", linewidth=0.7)


def plot_doenca_por_bairro(df_doenca_bairro, fig, ax):
    sns.barplot(
        data=df_doenca_bairro,
        x="Doença",
        y="Quantidade",
        hue="Bairro",
        errorbar=None,
        ax=ax,
    )

    ax.set_title("Quantidade de Doenças por Bairro")
    ax.set_xlabel("Doença")
    ax.set_ylabel("Quantidade de Incidências")
    ax.legend(title="Bairro")
    ax.grid(True, axis="y", linestyle="--", linewidth=0.7)
