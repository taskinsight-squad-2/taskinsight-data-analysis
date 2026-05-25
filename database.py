import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")
client = AsyncIOMotorClient(MONGODB_URL)
db = client["task_insight_db"]

#Função auxiliar para obter a coleção de métricas

async def get_analytics_collection():
    return db["analytics"]