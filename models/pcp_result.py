from sqlalchemy import Column, Integer, ForeignKey, JSON
from core.database import Base

class PCPResult(Base):
    __tablename__ = "pcp_results"

    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    result = Column(JSON)
