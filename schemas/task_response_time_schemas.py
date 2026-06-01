from pydantic import BaseModel, Field
from typing import List

class ResponseTimeMetrics(BaseModel):
    date: str = Field(..., description="Data no formato YYYY-MM-DD")
    slaPercentage: float = Field(..., description="Percentual de tarefas atendidas dentro do SLA")
    target: int = Field(..., description="Meta de SLA esperada (fixo em 90%)")

class StandardResponseTimeResponse(BaseModel):
    success: bool
    data: List[ResponseTimeMetrics]
