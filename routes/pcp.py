from uuid import uuid4

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


# 🔹 POST — CRIA CONTEXTO PCP
@router.post("/context")
def create_context(
    data: dict,
    company: Company = Depends(get_current_company),
    db: Session = Depends(get_db)
):
    context = PCPContext(
        company_id=company.id,
        payload=data
    )
    db.add(context)
    db.commit()
    db.refresh(context)

    return {
        "status": "created",
        "context_id": context.id,
        "company": company.name
    }


# 🔹 GET — BUSCA O ÚLTIMO CONTEXTO PCP
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


# 🔹 POST — EXECUTA O AGENTE PCP
@router.post("/run")
def run_pcp(
    company: Company = Depends(get_current_company),
    db: Session = Depends(get_db)
):
    # 1️⃣ Busca o último contexto
    ctx = (
        db.query(PCPContext)
        .filter(PCPContext.company_id == company.id)
        .order_by(PCPContext.created_at.desc())
        .first()
    )

    if not ctx:
        raise HTTPException(
            status_code=404,
            detail="Nenhum contexto PCP disponível"
        )

    payload = ctx.payload

    estoque = payload.get("estoque", 0)
    producao = payload.get("producao", 0)
    demanda = payload.get("demanda", 0)

    # 2️⃣ Regra simples de PCP (v1)
    if estoque + producao >= demanda:
        status = "ok"
        ajuste_producao = 0
        sugestao = "Produção atende a demanda"
    else:
        status = "ajuste_necessario"
        ajuste_producao = demanda - (estoque + producao)
        sugestao = f"Aumentar produção em {ajuste_producao} unidades"

    result = {
        "status": status,
        "estoque": estoque,
        "producao_atual": producao,
        "demanda": demanda,
        "ajuste_producao": ajuste_producao,
        "sugestao": sugestao
    }

    # 3️⃣ Prepara payload conforme contrato do service
    run_id = str(uuid4())

    payload_to_save = {
        "run_id": run_id,
        "agent_version": "pcp-v1",
        "result": result
    }

    # 4️⃣ Salva resultado
    save_pcp_result(
        db,
        company.id,
        payload_to_save
    )

    # 5️⃣ Retorna resposta ao caller (n8n, etc)
    return {
        "run_id": run_id,
        **result
    }
