from sqlalchemy import Column, Integer, JSON, ForeignKey, DateTime
from core.database import Base
from datetime import datetime

class PCPContext(Base):
    __tablename__ = "pcp_contexts"

    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    payload = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
