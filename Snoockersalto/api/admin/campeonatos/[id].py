from fastapi import FastAPI, HTTPException, Request
import hmac
import os
from bson import ObjectId
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


def oid(item_id: str) -> ObjectId:
    try:
        return ObjectId(item_id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")


@app.patch("/{item_id}")
@app.patch("/api/admin/campeonatos/{item_id}")
async def alternar(item_id: str, request: Request):
    check_admin(request)
    client, db = get_db()
    try:
        doc = await db.campeonatos.find_one({"_id": oid(item_id)})
        if not doc:
            raise HTTPException(status_code=404, detail="Campeonato não encontrado")
        novo = not doc.get("registration_open", True)
        await db.campeonatos.update_one({"_id": doc["_id"]}, {"$set": {"registration_open": novo}})
        return {"ok": True, "registration_open": novo}
    finally:
        client.close()


@app.delete("/{item_id}")
@app.delete("/api/admin/campeonatos/{item_id}")
async def excluir(item_id: str, request: Request):
    check_admin(request)
    client, db = get_db()
    try:
        res = await db.campeonatos.delete_one({"_id": oid(item_id)})
        if res.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Campeonato não encontrado")
        return {"ok": True}
    finally:
        client.close()
