from jose import jwt
from core.config import JWT_SECRET

def decode_token(token: str):
    return jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
