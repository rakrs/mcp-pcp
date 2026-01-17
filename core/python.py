import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost/mcp")
JWT_SECRET = os.getenv("JWT_SECRET", "super-secret-key")
