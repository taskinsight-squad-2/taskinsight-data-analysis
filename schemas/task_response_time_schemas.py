from pydantic import BaseModel, Field

from typing import List



  
class ResponseTimeMetrics(BaseModel):

    date: str = Field(...)
    sla_percentage: float = Field(...)