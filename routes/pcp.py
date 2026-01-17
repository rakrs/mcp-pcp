from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from core.database import SessionLocal
from core.security import decode_token
from services.pcp_service import save_pcp_result
from models.pcp_context import PCPContext

router = APIRouter(prefix="/mcp/pcp")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_company_id(authorization: str = Header(...)):
    try:
        token = authorization.replace("Bearer ", "")
        payload = decode_token(token)
        return payload["company_id"]
    except:
        raise HTTPException(status_code=401, detail="Token inválido")

@router.get("/context")
def get_context(db: Session = Depends(get_db), company_id: int = Depends(get_company_id)):
    ctx = db.query(PCPContext)\
        .filter(PCPContext.company_id == company_id)\
        .order_by(PCPContext.created_at.desc())\
        .first()

    if not ctx:
        raise HTTPException(status_code=404, detail="Contexto PCP não encontrado")

    return ctx.payload

@router.post("/result")
def save_result(data: dict, db: Session = Depends(get_db), company_id: int = Depends(get_company_id)):
    save_pcp_result(db, company_id, data)
    return {"status": "OK"}
