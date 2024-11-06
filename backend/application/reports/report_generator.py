# application/reports/report_generator.py

from fpdf import FPDF
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Relatório de Análise de Dados de Saúde', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(5)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()

    def add_image(self, image_path, x, y, w, h):
        self.image(image_path, x, y, w, h)

def generate_report(df, analysis_summary, output_path):
    pdf = PDF()
    pdf.add_page()

    # Adicionar título e resumo da análise
    pdf.chapter_title('Resumo da Análise')
    pdf.chapter_body(analysis_summary)

    # Adicionar tabela de dados
    pdf.chapter_title('Tabela de Dados')
    table_data = df.head(10).to_string(index=False)
    pdf.chapter_body(table_data)

    # Adicionar gráfico
    pdf.chapter_title('Gráfico de Distribuição')
    fig, ax = plt.subplots(figsize=(10, 6))
    df_pivot = pd.pivot_table(
        df,
        values="Doenca",
        index="Faixa Etária",
        columns="Sexo",
        aggfunc="count",
        fill_value=0,
        observed=False
    )
    sns.heatmap(df_pivot, annot=True, fmt="d", cmap="coolwarm", cbar=True, ax=ax)
    ax.set_title('Distribuição de Doenças por Faixa Etária e Gênero')
    image_path = 'heatmap.png'
    plt.savefig(image_path)
    pdf.add_image(image_path, 10, 100, 190, 100)
    os.remove(image_path)

    pdf.output(output_path)

# Exemplo de uso
if __name__ == "__main__":
    # Dados de exemplo
    data = {
        'Idade': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        'Sexo': ['M', 'F', 'M', 'F', 'M', 'F', 'M', 'F', 'M', 'F'],
        'Doenca': ['Gripe', 'Covid', 'Gripe', 'Covid', 'Gripe', 'Covid', 'Gripe', 'Covid', 'Gripe', 'Covid'],
        'Faixa Etária': ['Criança', 'Adolescente', 'Adulto', 'Meia-Idade', 'Idoso', 'Criança', 'Adolescente', 'Adulto', 'Meia-Idade', 'Idoso']
    }
    df = pd.DataFrame(data)
    analysis_summary = "Esta análise mostra a distribuição de doenças por faixa etária e gênero. Observa-se que a gripe é mais comum em crianças e idosos, enquanto a Covid é mais prevalente em adolescentes e adultos."
    output_path = 'relatorio_analise.pdf'
    generate_report(df, analysis_summary, output_path)