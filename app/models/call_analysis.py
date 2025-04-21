from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class CallAnalysisDB(Base):
    __tablename__ = "call_analysis"
    id = Column(Integer, primary_key=True, index=True)
    fileName = Column(String, nullable=False)
    dateAnalyzed = Column(String, nullable=False)
    status = Column(String, nullable=False)
    threatLevel = Column(String, nullable=False)
    callerNumber = Column(String, nullable=False)
    recipientNumber = Column(String, nullable=False)

    def as_dict(self):
        return {
            "id": self.id,
            "fileName": self.fileName,
            "dateAnalyzed": self.dateAnalyzed,
            "status": self.status,
            "threatLevel": self.threatLevel,
            "callerNumber": self.callerNumber,
            "recipientNumber": self.recipientNumber,
        }