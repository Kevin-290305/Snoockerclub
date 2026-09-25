import os
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI()

SEED = {
    "title": "Campeonato de Sinuca — Snooker Club Salto",
    "date": "Data a confirmar",
    "format": "Individual ou dupla",
    "prize": "A definir",
    "details": "Novos torneios são anunciados aqui, no Instagram e no WhatsApp do clube.",
    "registration_open": True,
}


def get_db():
    client = AsyncIOMotorClient(os.environ["MONGO_URL"])
    return client, client[os.environ.get("DB_NAME", "snooker")]


def limpa(doc):
    doc = dict(doc)
    doc["id"] = str(doc.pop("_id"))
    return doc


@app.get("/")
@app.get("/api/campeonatos")
async def listar():
    client, db = get_db()
    try:
        if await db.campeonatos.count_documents({}) == 0:
            await db.campeonatos.insert_one(dict(SEED))
        docs = await db.campeonatos.find({"registration_open": True}).sort("created_at", 1).to_list(200)
        return [limpa(d) for d in docs]
    finally:
        client.close()
