## Automação e Análise de Dados Hospitalares

Projeto de Análise e Automação de Dados Hospitalares

## 🏥 Proposta do Projeto

Este projeto foi desenvolvido para automatizar e analisar dados hospitalares, fornecendo insights essenciais para gestores e profissionais de saúde. A aplicação utiliza técnicas de ciência de dados para aprimorar a gestão hospitalar, especialmente no controle de ocupação de leitos, análise de incidência de doenças por faixa etária, gênero e localização, além de possibilitar a previsão de demandas futuras com base em dados históricos.

## 🏗️ Construção do Projeto e Aplicação

O projeto foi construído utilizando uma arquitetura modular, que facilita a escalabilidade e a manutenção. As principais etapas da construção do projeto incluem:

- **Coleta e Armazenamento de Dados**: Os dados são coletados de diferentes fontes e armazenados em um banco de dados central (SQLite, mas compatível com outros bancos de dados). A pasta `base_de_dados` contém scripts que atualizam e validam esses dados antes de serem usados para análise.
- **Análise de Dados**: A análise é conduzida utilizando bibliotecas de Python como Pandas para manipulação de dados e Statsmodels para modelagem de séries temporais (ARIMA). A análise é modular, dividida em componentes que processam dados demográficos, ocupação de leitos e incidência de doenças.
- **Visualização de Dados**: Gráficos e dashboards são criados utilizando Matplotlib e Streamlit para permitir uma interpretação visual das informações. Esses componentes estão organizados na pasta `reports`, que inclui scripts para geração de gráficos e relatórios automáticos.
- **Previsão de Ocupação**: O módulo de previsão utiliza modelos de séries temporais (ARIMA) para prever a ocupação de leitos. Essa previsão é essencial para o planejamento hospitalar e para evitar sobrecargas.
- **Geração de Relatórios**: Relatórios em formatos PDF e CSV são gerados automaticamente e armazenados no diretório `reports`, permitindo fácil compartilhamento e análise posterior.
- **Testes e Validação**: Uma suíte de testes foi implementada para garantir a robustez do sistema. Os testes estão na pasta `tests`, cobrindo desde a integridade do banco de dados até a geração de relatórios e desempenho das funções.

## Aplicação Prática

Este projeto é aplicável em cenários onde hospitais e clínicas precisam monitorar e prever a ocupação, além de entender melhor o perfil epidemiológico dos pacientes atendidos. Com base em dados históricos, o sistema permite tomar decisões informadas sobre alocação de recursos, planejamento de demanda e prevenção de surtos, especialmente em regiões com alta densidade populacional.

## 🔍 Principais Funcionalidades

- **Análise de Ocupação de Leitos**: Monitoramento histórico e previsão de ocupação.
- **Distribuição de Doenças por Faixa Etária e Gênero**: Análise demográfica para identificar tendências.
- **Distribuição de Doenças por Bairro**: Identificação de áreas com maior incidência de doenças.
- **Geração de Relatórios**: Relatórios automáticos para acompanhamento e planejamento estratégico.

## 📖 Fundamentos Teóricos

### Análise de Dados em Saúde Pública

A análise de dados em saúde pública envolve o processamento e a interpretação de grandes volumes de dados para identificar padrões e tendências. Isso inclui dados demográficos, histórico de ocupação, e registros de incidência de doenças. Esse tipo de análise é fundamental para:

- **Prevenção de Surtos**: Identificar áreas com alta incidência de doenças e prever a expansão de surtos.
- **Gestão de Recursos**: Otimizar a alocação de recursos hospitalares, como leitos, profissionais e equipamentos.
- **Tomada de Decisões**: Fornecer dados para decisões estratégicas, especialmente em períodos de alta demanda ou pandemias.

### Modelagem de Séries Temporais (ARIMA)

A previsão de demanda de leitos é feita com o modelo ARIMA (AutoRegressive Integrated Moving Average). O ARIMA é amplamente usado em previsões de séries temporais, devido à sua capacidade de lidar com padrões de tendência e sazonalidade, essenciais para prever a ocupação hospitalar em períodos futuros. A implementação do modelo ajuda a antecipar a necessidade de recursos em picos de demanda, como períodos de aumento de doenças sazonais.

### Visualização de Dados e Tomada de Decisões

A visualização de dados é um aspecto crucial para facilitar a interpretação rápida de grandes volumes de informações. Gráficos e dashboards permitem que os gestores hospitalares identifiquem rapidamente mudanças nas taxas de ocupação ou picos de incidência de doenças. O projeto utiliza Matplotlib e Streamlit para criar visualizações interativas, tornando o processo de tomada de decisão mais eficiente.

## ⚙️ Estrutura do Projeto

A organização do projeto está estruturada da seguinte forma:

```plaintext
📦 Automatizando_Dados
├── 📂 backend/
│   ├── 📂 application/
│   │   ├── 📂 api/
│   │   │   ├── routes.py                     # Configuração de rotas da API
│   │   │   └── views.py                      # Lógica de visualizações e endpoints
│   │   ├── 📂 base_de_dados/
│   │   │   └── update_data.py                # Atualização e manipulação de dados
│   │   ├── 📂 reports/
│   │   │   ├── analyze_occupacao_arima.py    # Previsão de ocupação com ARIMA
│   │   │   ├── dashboard.py                  # Dashboard interativo (Streamlit)
│   │   │   ├── generate_reports.py           # Geração de relatórios automáticos
│   │   │   └── visualize.py                  # Visualização de dados
│   │   ├── generate_atendimentos.py          # Geração de dados de atendimentos
│   │   ├── database.py                       # Configuração do banco de dados
│   │   ├── populate.py                       # Preenchimento inicial do banco de dados
│   │   ├── models.py                         # Modelos de dados
│   │   └── validators.py                     # Validações de dados
│   ├── main.py                               # Configuração principal do backend
├── 📂 instance/
│   └── your_database.db                      # Banco de dados SQLite local
├── 📂 reports/
│   ├── ocupacao_exemplo.png                  # Exemplo de gráfico de ocupação
│   ├── distribuicao_etaria_exemplo.png       # Exemplo de gráfico de distribuição etária
│   └── doenca_bairro_exemplo.png             # Exemplo de gráfico de distribuição por bairro
├── 📂 tests/
│   ├── test_database.py                      # Testes para o banco de dados
│   ├── test_exceptions.py                    # Testes de exceções
│   ├── test_performance.py                   # Testes de desempenho
│   ├── test_reports.py                       # Testes de geração de relatórios
│   └── test_update.py                        # Testes de atualização de dados
├── .gitignore                                # Arquivos e diretórios ignorados pelo Git
├── README.md                                 # Documentação do projeto
└── requirements.txt                          # Dependências do projeto
```

## 🚀 Principais Tecnologias Utilizadas

- **Python**: Linguagem principal do projeto.
- **SQLAlchemy**: ORM para manipulação de dados.
- **Flask**: Framework web para criação de APIs.
- **Pandas**: Manipulação e análise de dados.
- **Matplotlib & Seaborn**: Visualização gráfica.
- **Streamlit**: Dashboard interativo.
- **Statsmodels**: Modelagem de séries temporais (ARIMA).
- **FPDF**: Geração de relatórios em PDF.
- **Pytest**: Framework de testes.
- **SQLite**: Banco de dados local.
- **Git & GitHub**: Controle de versão e colaboração.
- **VSCode**: Editor de código preferencial.

## 📝 Requisitos e Instalação

### Pré-requisitos

- **Python 3.7+**
- Banco de dados configurado (ex.: SQLite, PostgreSQL, MySQL)

### Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/DaviSoaresDilly/Automatizando_dados
   cd Automatizando_dados
   ```

2. Crie e ative um ambiente virtual:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Para Windows: venv\Scripts\activate
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

## 🖥️ Como Utilizar o Projeto

### Configuração do Banco de Dados

- A configuração inicial do banco de dados pode ser feita utilizando os scripts em `backend/main.py`.

### Executando o Dashboard (Streamlit)

- Para visualizar as análises interativas, execute o comando:

  ```bash
  streamlit run backend/application/reports/dashboard.py
  ```

- Acesse o dashboard localmente em `http://localhost:8501`.

### Geração de Relatórios

- O script `generate_reports.py` permite a criação de relatórios de ocupação, distribuição por idade e gênero, e distribuição por bairro:

  ```bash
  python backend/application/reports/generate_reports.py
  ```

- Os relatórios são salvos na pasta `reports/` em formatos CSV e PDF, prontos para análise e compartilhamento.

## 📊 Descrição das Análises

### Ocupação de Leitos

Análise da ocupação histórica dos leitos em uma clínica e previsão de ocupação para um período futuro. Utiliza modelagem ARIMA para prever a demanda.

### Distribuição de Doenças por Faixa Etária e Gênero

Exibe as incidências de doenças em diferentes faixas etárias e gêneros, permitindo uma análise segmentada.

### Distribuição de Doenças por Bairro

Apresenta os bairros mais afetados por determinadas doenças, ajudando na identificação de áreas de alta incidência.

## 📂 Diretório de Relatórios

Os relatórios gerados são armazenados em `./reports/` com os seguintes formatos:

- **Ocupação de Leitos**: `ocupacao_report_{YYYYMMDD_HHMM}.csv` e `.pdf`
- **Distribuição por Faixa Etária e Gênero**: `distribuicao_faixa_etaria_sexo_{YYYYMMDD_HHMM}.csv` e `.pdf`
- **Distribuição de Doenças por Bairro**: `doenca_por_bairro_{YYYYMMDD_HHMM}.csv` e `.pdf`

## 📈 Exemplos de Gráficos

### Gráfico de Ocupação de Leitos

![Exemplo de Ocupação de Leitos](./reports/ocupacao_exemplo.png)

### Distribuição por Idade e Gênero

![Distribuição por Idade e Gênero](./reports/distribuicao_etaria_exemplo.png)

### Distribuição por Bairro

![Distribuição por Bairro](./reports/doenca_bairro_exemplo.png)

## 🧪 Testes

O projeto possui uma suíte de testes para verificar o funcionamento do sistema, localizada na pasta `tests/`. Os principais testes incluem:

- **test_database.py**: Verifica operações no banco de dados.
- **test_exceptions.py**: Testa o tratamento de exceções.
- **test_performance.py**: Avalia o desempenho das funções principais.
- **test_reports.py**: Valida a geração dos relatórios.
- **test_update.py**: Testa a funcionalidade de atualização de dados.

Para executar todos os testes, use o comando:

```bash
pytest
```

## 📋 Considerações Finais

Este projeto visa fornecer uma ferramenta eficaz para análise de dados hospitalares, com uma interface intuitiva e relatórios acionáveis. Futuras melhorias incluem a adição de análises preditivas e integração com sistemas de prontuário eletrônico.

---

## 🤝 Contribuições

Contribuições são bem-vindas! Para contribuir, abra uma _issue_ ou envie um _pull request_.

## 🛠️ Licença

Este projeto é licenciado sob a Licença MIT.
