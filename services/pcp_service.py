from sqlalchemy.orm import Session
from models.pcp_result import PCPResult

def save_pcp_result(db: Session, company_id: int, data: dict):
    result = PCPResult(
        company_id=company_id,
        run_id=data["run_id"],
        result=data["result"],
        agent_version=data["agent_version"]
    )
    db.add(result)
    db.commit()
