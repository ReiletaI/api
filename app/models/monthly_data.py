from pydantic import BaseModel

class MonthlyData(BaseModel):
    month: str
    callsAnalyzed: int