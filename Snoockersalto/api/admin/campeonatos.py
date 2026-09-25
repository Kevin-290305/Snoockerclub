from fastapi import FastAPI, Request
import hmac
import os
from pydantic import BaseModel
from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI()


def get_db():
    client = AsyncIOMotorClient(os.environ["MONGO_URL"])
    return client, client[os.environ.get("DB_NAME", "snooker")]


def check_admin(request: Request):
    pw = request.headers.get("x-admin-password", "")
    expected = os.environ.get("ADMIN_PASSWORD", "")
    if not expected or not hmac.compare_digest(pw, expected):
        from fastapi import HTTPException
        raise HTTPException(status_code=401, detail="Senha do painel incorreta")


def limpa(doc):
    doc = dict(doc)
    doc["id"] = str(doc.pop("_id"))
    return doc


class Campeonato(BaseModel):
    title: str
    date: str = "Data a confirmar"
    format: str = ""
    prize: str = ""
    details: str = ""


@app.get("/")
@app.get("/api/admin/campeonatos")
async def listar(request: Request):
    check_admin(request)
    client, db = get_db()
    try:
        docs = await db.campeonatos.find().sort("created_at", -1).to_list(200)
        return [limpa(d) for d in docs]
    finally:
        client.close()


@app.post("/")
@app.post("/api/admin/campeonatos")
async def criar(request: Request, camp: Campeonato):
    check_admin(request)
    doc = camp.model_dump()
    doc.setdefault("date", "Data a confirmar")
    doc["format"] = doc["format"] or ""
    doc["prize"] = doc["prize"] or ""
    doc["details"] = doc["details"] or ""
    doc["registration_open"] = True
    doc["created_at"] = datetime.now(timezone.utc).isoformat()
    client, db = get_db()
    try:
        res = await db.campeonatos.insert_one(doc)
        doc["_id"] = res.inserted_id
        return limpa(doc)
    finally:
        client.close()
