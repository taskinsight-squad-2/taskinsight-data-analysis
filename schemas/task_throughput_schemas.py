from pydantic import BaseModel, Field
from typing import List

class ThroughputItem(BaseModel):
    day: str = Field(..., description="Data no formato YYYY-MM-DD")
    count: int = Field(..., description="Quantidade de tarefas concluídas no dia")

class StandardThroughputResponse(BaseModel):
    success: bool
    data: List[ThroughputItem]
