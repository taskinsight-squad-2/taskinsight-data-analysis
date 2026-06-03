from pydantic import BaseModel, Field
from typing import List


class ResolutionTimeMetrics(BaseModel):
    date: str = Field(..., description="Data no formato YYYY-MM-DD")
    onTimeResolutions: float = Field(..., description="Percentual de tarefas resolvidas dentro do prazo")    
    target: int = Field(..., description="Meta de resolução esperada (fixo em 90%)")

class StandardResolutionTimeResponse(BaseModel):
    success: bool
    data: List[ResolutionTimeMetrics]
    
    