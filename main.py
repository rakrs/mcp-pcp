from fastapi import FastAPI

# IMPORTA TODOS OS MODELS (OBRIGATÓRIO)
from models.company import Company
from models.pcp_context import PCPContext
from models.pcp_result import PCPResult

from core.database import Base, engine
from routes.pcp import router as pcp_router

app = FastAPI(title="MCP Server")

# REGISTRA ROTAS
app.include_router(pcp_router)

# AGORA SIM CRIA AS TABELAS
Base.metadata.create_all(bind=engine)
