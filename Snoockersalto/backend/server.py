from fastapi import FastAPI, APIRouter, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field, ConfigDict, BeforeValidator
from typing import Optional, List, Annotated
import os
import hmac
import logging
from pathlib import Path
from datetime import datetime, timezone
from bson import ObjectId


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

app = FastAPI()
api_router = APIRouter(prefix="/api")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ---------- Modelos (padrão BaseDocument) ----------

PyObjectId = Annotated[str, BeforeValidator(lambda v: str(v))]


class BaseDocument(BaseModel):
    model_config = ConfigDict(extra="ignore", populate_by_name=True)
    id: Optional[PyObjectId] = Field(default=None, alias="_id")

    def to_mongo(self):
        data = self.model_dump(exclude_none=True)
        data.pop("id", None)
        return data

    @classmethod
    def from_mongo(cls, doc):
        if doc is None:
            return None
        doc = dict(doc)
        doc["_id"] = str(doc["_id"])
        return cls(**doc)


def now_iso():
    return datetime.now(timezone.utc).isoformat()


class Championship(BaseDocument):
    title: str
    date: str = "Data a confirmar"
    format: str = "Individual ou dupla"
    prize: str = "A definir"
    details: str = ""
    registration_open: bool = True
    created_at: str = Field(default_factory=now_iso)


class ChampionshipCreate(BaseModel):
    title: str
    date: str = "Data a confirmar"
    format: str = ""
    prize: str = ""
    details: str = ""


class Registration(BaseDocument):
    modalidade: str
    nome: str
    idade: int
    sexo: str
    campeonato: str
    telefone: str
    cidade: str = ""
    obs: str = ""
    created_at: str = Field(default_factory=now_iso)


class RegistrationCreate(BaseModel):
    modalidade: str
    nome: str
    idade: int
    sexo: str
    campeonato: str
    telefone: str
    cidade: str = ""
    obs: str = ""


# ---------- Autenticação simples do painel (senha única do .env) ----------

def check_admin(request: Request):
    pw = request.headers.get("x-admin-password", "")
    expected = os.environ.get("ADMIN_PASSWORD", "")
    if not expected or not hmac.compare_digest(pw, expected):
        raise HTTPException(status_code=401, detail="Senha do painel incorreta")


# ---------- Rotas públicas ----------

@api_router.get("/")
async def root():
    return {"message": "Snooker Club Salto API"}


@api_router.get("/campeonatos", response_model=List[Championship], response_model_by_alias=False)
async def list_campeonatos():
    docs = await db.campeonatos.find({"registration_open": True}).sort("created_at", 1).to_list(200)
    return [Championship.from_mongo(d) for d in docs]


@api_router.post("/inscricoes", response_model=Registration, response_model_by_alias=False)
async def create_inscricao(input: RegistrationCreate):
    reg = Registration(**input.model_dump())
    result = await db.inscricoes.insert_one(reg.to_mongo())
    reg.id = str(result.inserted_id)
    logger.info(f"Nova inscrição: {reg.nome} -> {reg.campeonato}")
    return reg


# ---------- Rotas do painel (protegidas por senha) ----------

@api_router.post("/admin/login")
async def admin_login(request: Request):
    check_admin(request)
    return {"ok": True}


@api_router.get("/admin/campeonatos", response_model=List[Championship], response_model_by_alias=False)
async def admin_list_campeonatos(request: Request):
    check_admin(request)
    docs = await db.campeonatos.find().sort("created_at", -1).to_list(200)
    return [Championship.from_mongo(d) for d in docs]


@api_router.post("/admin/campeonatos", response_model=Championship, response_model_by_alias=False)
async def admin_create_campeonato(request: Request, input: ChampionshipCreate):
    check_admin(request)
    camp = Championship(**input.model_dump())
    result = await db.campeonatos.insert_one(camp.to_mongo())
    camp.id = str(result.inserted_id)
    logger.info(f"Campeonato criado: {camp.title}")
    return camp


def parse_oid(item_id: str) -> ObjectId:
    try:
        return ObjectId(item_id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")


@api_router.patch("/admin/campeonatos/{item_id}")
async def admin_toggle_campeonato(item_id: str, request: Request):
    check_admin(request)
    doc = await db.campeonatos.find_one({"_id": parse_oid(item_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Campeonato não encontrado")
    novo = not doc.get("registration_open", True)
    await db.campeonatos.update_one({"_id": doc["_id"]}, {"$set": {"registration_open": novo}})
    return {"ok": True, "registration_open": novo}


@api_router.delete("/admin/campeonatos/{item_id}")
async def admin_delete_campeonato(item_id: str, request: Request):
    check_admin(request)
    res = await db.campeonatos.delete_one({"_id": parse_oid(item_id)})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Campeonato não encontrado")
    return {"ok": True}


@api_router.get("/admin/inscricoes", response_model=List[Registration], response_model_by_alias=False)
async def admin_inscricoes(request: Request):
    check_admin(request)
    docs = await db.inscricoes.find().sort("created_at", -1).to_list(500)
    return [Registration.from_mongo(d) for d in docs]


@api_router.delete("/admin/inscricoes/{item_id}")
async def admin_delete_inscricao(item_id: str, request: Request):
    check_admin(request)
    res = await db.inscricoes.delete_one({"_id": parse_oid(item_id)})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Inscrição não encontrada")
    return {"ok": True}


# ---------- Inicialização ----------

@app.on_event("startup")
async def seed_campeonatos():
    try:
        if await db.campeonatos.count_documents({}) == 0:
            camp = Championship(
                title="Campeonato de Sinuca — Snooker Club Salto",
                date="Data a confirmar",
                format="Individual ou dupla",
                prize="A definir",
                details="Novos torneios são anunciados aqui, no Instagram e no WhatsApp do clube.",
            )
            await db.campeonatos.insert_one(camp.to_mongo())
            logger.info("Campeonato de exemplo criado (removível pelo painel)")
    except Exception as e:
        logger.warning(f"MongoDB indisponível ao iniciar (o site funciona; salvar campeonatos não): {e}")


@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()


app.include_router(api_router)

# Sirve o site (pasta Snoockersalto) na mesma porta da API —
# permite rodar tudo com um só comando na máquina local.
SITE_DIR = ROOT_DIR.parent / "Snoockersalto"
if SITE_DIR.exists():
    app.mount("/", StaticFiles(directory=str(SITE_DIR), html=True), name="site")

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)
