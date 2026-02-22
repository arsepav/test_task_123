from fastapi import Header, HTTPException
from app.config import settings


async def verify_api_key(x_api_key: str = Header(..., description="Static API key")):
    if x_api_key != settings.api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key
