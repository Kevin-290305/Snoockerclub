import hmac
import os
from fastapi import FastAPI, HTTPException, Request

app = FastAPI()


@app.post("/")
@app.post("/api/admin/login")
async def login(request: Request):
    pw = request.headers.get("x-admin-password", "")
    expected = os.environ.get("ADMIN_PASSWORD", "")
    if not expected or not hmac.compare_digest(pw, expected):
        raise HTTPException(status_code=401, detail="Senha do painel incorreta")
    return {"ok": True}
