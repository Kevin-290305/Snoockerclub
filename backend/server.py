from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
import os
import logging
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.get("/api/")
async def root():
    return {"message": "Snooker Club Salto API"}


# O site não usa banco de dados: os campeonatos ficam no arquivo
# js/campeonatos.js (estático). O backend só serve o site numa porta só
# para o teste local — nada é armazenado no servidor.
SITE_DIR = ROOT_DIR.parent / "Snoockersalto"
FRONTEND_PUBLIC = ROOT_DIR.parent / "frontend" / "public"
if SITE_DIR.exists():
    app.mount("/", StaticFiles(directory=str(SITE_DIR), html=True), name="site")
elif FRONTEND_PUBLIC.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_PUBLIC), html=True), name="site")

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)
