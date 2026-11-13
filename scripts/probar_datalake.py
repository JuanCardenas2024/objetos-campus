from pathlib import Path
from app.datalake.storage import subir_foto


def main():
    ruta = Path("prueba.jpg")
    if not ruta.exists():
        print("Coloca una imagen llamada prueba.jpg en la carpeta raíz del proyecto.")
        return

    url = subir_foto(ruta.read_bytes(), "image/jpeg")
    print("Foto guardada en:", url)


if __name__ == "__main__":
    main()