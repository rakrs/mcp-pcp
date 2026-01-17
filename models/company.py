import uuid
from sqlalchemy import Column, Integer, String
from core.database import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    api_key = Column(String, unique=True, nullable=False, index=True)

    @staticmethod
    def generate_api_key() -> str:
        return uuid.uuid4().hex
