# Automação e Análise de Dados Hospitalares

### Projeto de Análise e Automação de Dados Hospitalares

## 🏥 Proposta do Projeto

Este projeto foi desenvolvido para automatizar e analisar dados hospitalares, com foco em fornecer insights que ajudem no gerenciamento de ocupação de leitos, distribuição de doenças e monitoramento de incidência por faixa etária, gênero e localização. Utilizando técnicas de visualização e análise de séries temporais, o sistema oferece informações úteis para profissionais de saúde e gestores hospitalares, possibilitando uma visão abrangente do cenário de saúde em diferentes regiões.

## 🔍 Principais Funcionalidades

1. **Análise de Ocupação de Leitos**: Visualização da ocupação histórica e previsão para auxiliar na gestão de capacidade hospitalar.
2. **Distribuição de Doenças por Faixa Etária e Gênero**: Análise demográfica que exibe a distribuição de doenças entre diferentes grupos etários e gêneros.
3. **Distribuição de Doenças por Bairro**: Identifica as regiões mais afetadas e as doenças predominantes em cada área.
4. **Geração de Relatórios**: Relatórios automáticos em formatos PDF e CSV, armazenados em um diretório específico para fácil acesso.

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
│   │   |   ├── analyze_occupacao_arima.py    # Previsão de ocupação com ARIMA
│   │   |   ├── dashboard.py                  # Dashboard interativo (Streamlit)
│   │   |   ├── generate_reports.py           # Geração de relatórios automáticos
│   │   |   └── visualize.py                  # Visualização de dados
|   |   ├── generate_atendimentos.py          # Geração de dados de atendimentos
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
