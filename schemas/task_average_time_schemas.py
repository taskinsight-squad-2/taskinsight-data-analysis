from pydantic import BaseModel, Field

class TaskAverageTimeResponse(BaseModel):
    average_time_seconds: float = Field(..., description="Tempo médio em segundos para conclusão das tarefas")
    average_time_hours: float = Field(..., description="Tempo médio em horas para conclusão das tarefas")
    average_time_days: float = Field(..., description="Tempo médio em dias para conclusão das tarefas") 

class StandardAverageTimeResponse(BaseModel):
    success: bool
    data: TaskAverageTimeResponse    