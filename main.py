from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from database import client
from routes.task_metrics_routes import router as tasks_metrics_router



@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await client.admin.command('ping')
        print("Conexão com MongoDB estabelecida com sucesso.")
    except Exception as e:
        print(f"Erro ao conectar ao MongoDB: {e}")

    yield
    client.close()
    print("Conexão com MongoDB encerrada.")



app = FastAPI(
    title="TaskInsight Analytics API",
    description="API de análise de dados e métricas do TaskInsight",
    version="1.0.0",
    lifespan=lifespan
)



@app.get("/")
async def home():
    return {"message": "Bem-vindo à API do TaskInsight",
            "Status":"Online",
            "Ambiente":"Desenvolvimento"
            }

@app.get("/health")
async def health_check():
    return {"status": "ok"}

app.include_router(
    tasks_metrics_router
)
