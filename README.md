# taskinsight-data-analysis

API de análise de dados e métricas do TaskInsight, responsável por processar e expor métricas das tarefas armazenadas no MongoDB.

## Tecnologias

- [FastAPI](https://fastapi.tiangolo.com/)
- [Motor](https://motor.readthedocs.io/) (MongoDB async)
- [Python 3.11+](https://www.python.org/)

## Pré-requisitos

- Python 3.11+
- MongoDB
- pip

## Instalação

```bash
# Clone o repositório
git clone https://github.com/taskinsight-squad-2/taskinsight-data-analysis.git
cd taskinsight-data-analysis

# Crie e ative o ambiente virtual
python -m venv .venv
.venv\Scripts\activate  # Windows

# Instale as dependências
pip install -r requirements.txt
```

## Configuração

Crie um arquivo `.env` na raiz do projeto:

```env
MONGODB_URL=mongodb://localhost:27017
```

## Executando

```bash
fastapi dev main.py
```

A API estará disponível em `http://127.0.0.1:8000`  
Documentação Swagger em `http://127.0.0.1:8000/docs`

## Estrutura

```
├── core/
├── pipelines/
├── repositories/
├── routes/
├── schemas/
├── services/
├── database.py
└── main.py
```

## Observação

Esta API é responsável **apenas por métricas e análise de dados**. O CRUD das tarefas é gerenciado por uma API separada.
