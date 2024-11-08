# application/reports/report_generator.py

from fpdf import FPDF
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

# Classe para gerar o PDF
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Relatório de Análise de Dados de Saúde', 0, 1, 'C')

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

# Função para gerar o relatório
def generate_report(df, analysis_summary, output_path_pdf, output_path_csv, period_label):
    pdf = PDF()
    pdf.add_page()

    # Adicionar Introdução
    pdf.chapter_title('Introdução')
    introduction = (
        "Este relatório apresenta uma análise detalhada dos dados de saúde coletados, "
        "focando na distribuição de doenças por faixa etária e gênero. O objetivo é "
        "identificar padrões e tendências que possam informar decisões estratégicas em "
        "saúde pública."
    )
    pdf.chapter_body(introduction)

    # Adicionar Metodologia
    pdf.chapter_title('Metodologia')
    methodology = (
        "Os dados foram coletados de registros hospitalares e incluem informações sobre "
        "idade, gênero e tipo de doença dos pacientes. A análise descritiva foi realizada "
        "para identificar a distribuição de doenças por diferentes faixas etárias e gêneros. "
        "Foram utilizados gráficos de calor para visualizar os dados."
    )
    pdf.chapter_body(methodology)

    # Adicionar Resultados
    pdf.chapter_title('Resultados')
    pdf.chapter_body(analysis_summary)

    # Adicionar gráfico de heatmap
    if 'Doenca' in df.columns:
        pdf.add_page()
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
        pdf.add_image(image_path, 10, 50, 190, 100)
        os.remove(image_path)

    # Adicionar Discussão
    pdf.add_page()
    pdf.chapter_title('Discussão')
    discussion = (
        "Os resultados mostram que a gripe é mais comum em crianças e idosos, enquanto a Covid "
        "é mais prevalente em adolescentes e adultos. Esses padrões podem ser explicados por "
        "fatores como a maior exposição das crianças a ambientes escolares e a maior vulnerabilidade "
        "dos idosos. A prevalência da Covid em adolescentes e adultos pode estar relacionada a "
        "maiores níveis de interação social e mobilidade."
    )
    pdf.chapter_body(discussion)

    # Adicionar Conclusão
    pdf.chapter_title('Conclusão')
    conclusion = (
        "Esta análise fornece insights valiosos sobre a distribuição de doenças por faixa etária e gênero. "
        "Essas informações podem ser usadas para direcionar esforços de prevenção e alocação de recursos "
        "de maneira mais eficaz. Recomenda-se a continuidade do monitoramento e a realização de análises "
        "periódicas para acompanhar as mudanças nos padrões de saúde da população."
    )
    pdf.chapter_body(conclusion)

    # Salvar o PDF na pasta reports
    if not os.path.exists('reports'):
        os.makedirs('reports')
    pdf.output(os.path.join('reports', output_path_pdf))

    # Salvar a tabela de dados em CSV na pasta reports
    df.to_csv(os.path.join('reports', output_path_csv), index=False)

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
    period_label = "2024"
    output_path_pdf = f'relatorio_analise_{period_label}.pdf'
    output_path_csv = f'tabela_dados_{period_label}.csv'
    generate_report(df, analysis_summary, output_path_pdf, output_path_csv, period_label)