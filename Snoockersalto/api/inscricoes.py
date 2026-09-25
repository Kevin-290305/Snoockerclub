from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime, timezone
import os
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI()


def get_db():
    client = AsyncIOMotorClient(os.environ["MONGO_URL"])
    return client, client[os.environ.get("DB_NAME", "snooker")]


def limpa(doc):
    doc = dict(doc)
    doc["id"] = str(doc.pop("_id"))
    return doc


class Inscricao(BaseModel):
    modalidade: str
    nome: str
    idade: int
    sexo: str
    campeonato: str
    telefone: str
    cidade: str = ""
    obs: str = ""


@app.post("/")
@app.post("/api/inscricoes")
async def criar(insc: Inscricao):
    doc = insc.model_dump()
    doc["created_at"] = datetime.now(timezone.utc).isoformat()
    client, db = get_db()
    try:
        res = await db.inscricoes.insert_one(doc)
        doc["_id"] = res.inserted_id
        return limpa(doc)
    finally:
        client.close()
