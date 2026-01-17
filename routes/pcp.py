from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.database import SessionLocal
from core.auth import get_current_company

from models.company import Company
from models.pcp_context import PCPContext
from services.pcp_service import save_pcp_result

router = APIRouter(prefix="/mcp/pcp", tags=["PCP"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/context")
def get_context(
    company: Company = Depends(get_current_company),
    db: Session = Depends(get_db)
):
    ctx = (
        db.query(PCPContext)
        .filter(PCPContext.company_id == company.id)
        .order_by(PCPContext.created_at.desc())
        .first()
    )

    if not ctx:
        raise HTTPException(
            status_code=404,
            detail="Contexto PCP não encontrado"
        )

    return ctx.payload


@router.post("/result")
def save_result(
    data: dict,
    company: Company = Depends(get_current_company),
    db: Session = Depends(get_db)
):
    save_pcp_result(
        db=db,
        company_id=company.id,
        payload=data
    )

    return {"status": "OK"}
