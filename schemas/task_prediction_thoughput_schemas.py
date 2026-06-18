from pydantic import BaseModel
from typing import List


class ThroughputItem(BaseModel):
    day: str
    count: int


class ThroughputMetadata(BaseModel):
    average: float
    daysAnalysed: int


class ThroughputResponse(BaseModel):
    forecast: List[ThroughputItem]
    metadata: ThroughputMetadata


class StandardThroughputResponse(BaseModel):
    success: bool
    data: ThroughputResponse