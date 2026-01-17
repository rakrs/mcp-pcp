from sqlalchemy import Column, Integer, String
from core.database import Base

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    api_key = Column(String, unique=True)
