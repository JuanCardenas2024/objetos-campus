from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from app.config import settings
from app.health import estado_general
from app.routers import admin, auth, reportes

app = FastAPI(title="Sistema de Objetos Perdidos - Campus")
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)
app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).resolve().parent / "static"),
    name="static",
)

app.include_router(auth.router)
app.include_router(reportes.router)
app.include_router(admin.router)


@app.get("/health")
def health():
    resultado = estado_general()
    return {k: {"ok": ok, "detalle": msg} for k, (ok, msg) in resultado.items()}