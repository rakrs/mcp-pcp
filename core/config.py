import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://dummy")
JWT_SECRET = os.getenv("JWT_SECRET", "changeme")