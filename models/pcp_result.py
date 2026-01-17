from sqlalchemy import Column, Integer, JSON, ForeignKey, DateTime, String
from core.database import Base
from datetime import datetime

class PCPResult(Base):
    __tablename__ = "pcp_results"

    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    run_id = Column(String)
    result = Column(JSON)
    agent_version = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
