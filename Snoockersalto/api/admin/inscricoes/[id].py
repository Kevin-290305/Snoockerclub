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


@app.delete("/{item_id}")
@app.delete("/api/admin/inscricoes/{item_id}")
async def excluir(item_id: str, request: Request):
    check_admin(request)
    try:
        target = ObjectId(item_id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")
    client, db = get_db()
    try:
        res = await db.inscricoes.delete_one({"_id": target})
        if res.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Inscrição não encontrada")
        return {"ok": True}
    finally:
        client.close()
