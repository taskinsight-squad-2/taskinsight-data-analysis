from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import HTTPBearer
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from database import client
from routes.task_metrics_routes import router as tasks_metrics_router
from routes.task_predictions_routers import router as tasks_predictions_router




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
    lifespan=lifespan,
    swagger_ui_parameters={
        "persistAuthorization": True,
    }
)

security = HTTPBearer()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_openapi():
    if not app.openapi_schema:
        from fastapi.openapi.utils import get_openapi
        app.openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            description=app.description,
            routes=app.routes,
        )
        app.openapi_schema["components"]["securitySchemes"] = {
            "HTTPBearer": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
                "description": "Insira seu token JWT aqui"
            }
        }
    return app.openapi_schema


app.openapi = get_openapi




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
app.include_router(
    tasks_predictions_router
)
