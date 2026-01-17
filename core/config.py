import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgres://postgres:rFbwXV3N5diojFQtLfmZOMBDlHgpBFeZHxBlAuqDWkg8S7GAx46Cgu07s5YIKC6K@jcgkc0s44wkowcogwcc8gswk:5432/postgres")
JWT_SECRET = os.getenv("JWT_SECRET", "changeme")