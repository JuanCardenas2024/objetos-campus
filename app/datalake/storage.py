import uuid
from pathlib import Path
from app.config import settings

FORMATOS = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
}
TAMANO_MAXIMO = 5 * 1024 * 1024  # 5 MB


def _carpeta_fotos() -> Path:
    carpeta = Path(settings.DATALAKE_PATH) / "fotos"
    carpeta.mkdir(parents=True, exist_ok=True)
    return carpeta


def verificar_datalake() -> bool:
    ruta = Path(settings.DATALAKE_PATH)
    ruta.mkdir(parents=True, exist_ok=True)
    prueba = ruta / ".check"
    prueba.write_text("ok", encoding="utf-8")
    prueba.unlink()
    return True


def subir_foto(contenido: bytes, content_type: str) -> str:
    if content_type not in FORMATOS:
        raise ValueError("Formato no permitido. Usa JPG, PNG o WEBP.")
    if len(contenido) > TAMANO_MAXIMO:
        raise ValueError("La foto supera 5 MB.")

    nombre = f"{uuid.uuid4().hex}{FORMATOS[content_type]}"
    (_carpeta_fotos() / nombre).write_bytes(contenido)
    return f"fotos/{nombre}"