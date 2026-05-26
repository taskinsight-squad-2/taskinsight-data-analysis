import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")
client = AsyncIOMotorClient(MONGODB_URL)
db = client["TaskInsight"]

# Função auxiliar para obter a coleção de tarefas

async def get_tasks_collection():
    return db["tasks"]