from pydantic import BaseModel

class DashboardStats(BaseModel):
    totalCallsAnalyzed: int
    threatsDetected: int
    threatsVerified: int
    pendingVerification: int