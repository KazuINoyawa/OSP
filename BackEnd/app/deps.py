import os
from fastapi import Header, HTTPException

def get_api_token(authorization: str | None = Header(default=None)):
    """Simple API token check. Expect header: Authorization: Bearer <token>

    Token value is taken from env var `API_TOKEN` or defaults to 'dev-token'.
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != 'bearer':
        raise HTTPException(status_code=401, detail="Invalid Authorization header format")
    token = parts[1]
    expected = os.environ.get('API_TOKEN', 'dev-token')
    if token != expected:
        raise HTTPException(status_code=403, detail="Invalid API token")
    return token
