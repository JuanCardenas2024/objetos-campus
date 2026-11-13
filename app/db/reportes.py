from datetime import datetime
from bson import ObjectId
from app.db.mongo import get_db


def insertar_reporte(documento: dict) -> str:
    documento["creado_en"] = datetime.now()
    resultado = get_db()["reportes"].insert_one(documento)
    return str(resultado.inserted_id)


def obtener_reporte(reporte_id: str) -> dict | None:
    return get_db()["reportes"].find_one({"_id": ObjectId(reporte_id)})


def listar_reportes(filtro: dict) -> list[dict]:
    return list(get_db()["reportes"].find(filtro).sort("fecha", -1))


def marcar_reclamado(reporte_id: str, reclamo: dict) -> None:
    get_db()["reportes"].update_one(
        {"_id": ObjectId(reporte_id)},
        {"$set": {"estado": "reclamado", "reclamo": reclamo}},
    )


def actualizar_reclamo(reporte_id: str, campos: dict) -> None:
    # Cambia solo los campos enviados dentro de "reclamo"
    get_db()["reportes"].update_one(
        {"_id": ObjectId(reporte_id)},
        {"$set": {f"reclamo.{k}": v for k, v in campos.items()}},
    )


def revertir_reclamo(reporte_id: str) -> None:
    get_db()["reportes"].update_one(
        {"_id": ObjectId(reporte_id)},
        {"$set": {"estado": "pendiente"}, "$unset": {"reclamo": ""}},
    )