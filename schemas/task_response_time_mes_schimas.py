from pydantic import BaseModel, Field
from typing import List



class ResponseTimeMesMetrics(BaseModel):
    month: str = Field(..., description="Mês no formato YYYY-MM")
    slaPercentage: float = Field(..., description="Percentual de tarefas atendidas dentro do SLA")
    target: int = Field(..., description="Meta de SLA esperada (fixo em 90%)")

class StandardResponseTimeMesResponse(BaseModel):
    success: bool
    data: List[ResponseTimeMesMetrics]