from pydantic import BaseModel
from typing import Literal

class CallAnalysis(BaseModel):
    id: str
    fileName: str
    dateAnalyzed: str
    status: Literal["verified", "pending", "false_positive"]
    threatLevel: Literal["high", "medium", "low"]
    callerNumber: str
    recipientNumber: str