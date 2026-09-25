from fastapi import FastAPI, HTTPException, Request
import hmac
import os
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI()


def get_db():
    client = AsyncIOMotorClient(os.environ["MONGO_URL"])
    return client, client[os.environ.get("DB_NAME", "snooker")]


def check_admin(request: Request):
    pw = request.headers.get("x-admin-password", "")
    expected = os.environ.get("ADMIN_PASSWORD", "")
    if not expected or not hmac.compare_digest(pw, expected):
        raise HTTPException(status_code=401, detail="Senha do painel incorreta")


def limpa(doc):
    doc = dict(doc)
    doc["id"] = str(doc.pop("_id"))
    return doc


@app.get("/")
@app.get("/api/admin/inscricoes")
async def listar(request: Request):
    check_admin(request)
    client, db = get_db()
    try:
        docs = await db.inscricoes.find().sort("created_at", -1).to_list(500)
        return [limpa(d) for d in docs]
    finally:
        client.close()
