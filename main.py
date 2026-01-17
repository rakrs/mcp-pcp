from fastapi import FastAPI
from sqlalchemy import text

from core.database import Base, engine
from routes.pcp import router as pcp_router

# IMPORTA TODOS OS MODELS (OBRIGATÓRIO PARA O SQLALCHEMY)
from models.company import Company
from models.pcp_context import PCPContext
from models.pcp_result import PCPResult

app = FastAPI(title="MCP Server")

# REGISTRA AS ROTAS
app.include_router(pcp_router)

# CRIA AS TABELAS NO STARTUP
Base.metadata.create_all(bind=engine)


@app.get("/health")
def healthcheck():
    """
    Healthcheck para Coolify / Monitoramento
    """
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {
            "status": "ok",
            "database": "connected"
        }
    except Exception as e:
        return {
            "status": "error",
            "database": "disconnected",
            "detail": str(e)
        }
