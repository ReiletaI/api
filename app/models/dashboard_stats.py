from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class DashboardStatsDB(Base):
    __tablename__ = "dashboard_stats"

    id = Column(Integer, primary_key=True, index=True)
    totalCallsAnalyzed = Column(Integer, nullable=False)
    threatsDetected = Column(Integer, nullable=False)
    threatsVerified = Column(Integer, nullable=False)
    pendingVerification = Column(Integer, nullable=False)

    def as_dict(self):
        return {
            "id": self.id,
            "totalCallsAnalyzed": self.totalCallsAnalyzed,
            "threatsDetected": self.threatsDetected,
            "threatsVerified": self.threatsVerified,
            "pendingVerification": self.pendingVerification,
        }