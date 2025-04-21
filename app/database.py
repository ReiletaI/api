from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    from app.models.call_analysis import Base as CallAnalysisBase
    # Create only the call_analysis table; stats and monthly data are derived dynamically
    CallAnalysisBase.metadata.create_all(bind=engine)

def init_db_full():
    from app.models import call_analysis, dashboard_stats, monthly_data
    Base.metadata.create_all(bind=engine)