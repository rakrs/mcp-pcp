from sqlalchemy import Column, Integer, String, ForeignKey, JSON, DateTime
from sqlalchemy.sql import func

from core.database import Base


class PCPResult(Base):
    __tablename__ = "pcp_results"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)

    run_id = Column(String, unique=True, nullable=False)   # ✅ ADICIONE ISSO
    agent_version = Column(String, nullable=False)
    result = Column(JSON, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
