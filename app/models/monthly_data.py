from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class MonthlyDataDB(Base):
    __tablename__ = "monthly_data"
    id = Column(Integer, primary_key=True, index=True)
    month = Column(String, nullable=False)
    callsAnalyzed = Column(Integer, nullable=False)

    def as_dict(self):
        return {
            "id": self.id,
            "month": self.month,
            "callsAnalyzed": self.callsAnalyzed,
        }