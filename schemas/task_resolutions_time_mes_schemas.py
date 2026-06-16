from pydantic import BaseModel, Field
from typing import List

class ResolutionTimeMesMetrics(BaseModel):
    month: str = Field(..., description="Mês no formato YYYY-MM")
    onTimeSolution: float = Field(..., description="Percentual de tarefas resolvidas dentro do prazo")
    target: int = Field(..., description="Meta de resolução esperada (fixo em 90%)")

class StandardResolutionTimeMesResponse(BaseModel):
    success: bool
    data: List[ResolutionTimeMesMetrics]

