from fastapi import Header, HTTPException, Depends
from sqlalchemy.orm import Session

from core.database import SessionLocal
from models.company import Company


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_company(
    x_api_key: str = Header(..., alias="X-API-Key"),
    db: Session = Depends(get_db)
) -> Company:
    company = db.query(Company).filter(
        Company.api_key == x_api_key
    ).first()

    if not company:
        raise HTTPException(
            status_code=401,
            detail="Invalid API Key"
        )

    return company
