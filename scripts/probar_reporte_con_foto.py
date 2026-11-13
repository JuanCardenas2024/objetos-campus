from datetime import datetime
from pathlib import Path
from app.datalake.storage import subir_foto
from app.db.reportes import insertar_reporte, obtener_reporte


def main():
    foto = Path("prueba.jpg")
    if not foto.exists():
        print("Falta prueba.jpg en la carpeta raíz del proyecto.")
        return

    # 1. Guardar la foto en el datalake
    foto_url = subir_foto(foto.read_bytes(), "image/jpeg")

    # 2. Guardar el reporte en Mongo con esa ruta
    reporte_id = insertar_reporte({
        "tipo": "hallazgo",
        "objeto": "Audífonos negros",
        "descripcion": "Cafetería, mesa junto a la ventana",
        "sede": "Sede Sur",
        "fecha": datetime(2026, 11, 11),
        "hora": "09:15",
        "foto_url": foto_url,
        "usuario_id": 7,
        "estado": "pendiente",
    })

    # 3. Leer el reporte para comprobar
    reporte = obtener_reporte(reporte_id)
    print("Reporte creado:", reporte_id)
    print("foto_url guardada:", reporte["foto_url"])


if __name__ == "__main__":
    main()