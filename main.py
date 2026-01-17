from fastapi import FastAPI
from routes.pcp import router as pcp_router
from core.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="MCP Server")

app.include_router(pcp_router)
