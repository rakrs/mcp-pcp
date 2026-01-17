from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import SessionLocal
from models.company import Company

router = APIRouter(prefix="/companies", tags=["Companies"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_company(name: str, db: Session = Depends(get_db)):
    company = Company(
        name=name,
        api_key=Company.generate_api_key()
    )
    db.add(company)
    db.commit()
    db.refresh(company)

    return {
        "id": company.id,
        "name": company.name,
        "api_key": company.api_key
    }
