from app.db.mariadb import get_connection


def obtener_o_crear_usuario(tipo, cargo_personal, nombre_completo,
                            correo, identificacion, telefono) -> int:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id FROM usuarios WHERE correo_institucional = %s",
                (correo,),
            )
            fila = cur.fetchone()
            if fila:
                return fila["id"]

            cur.execute(
                """INSERT INTO usuarios
                   (tipo, cargo_personal, nombre_completo,
                    correo_institucional, identificacion, telefono)
                   VALUES (%s, %s, %s, %s, %s, %s)""",
                (tipo, cargo_personal, nombre_completo,
                 correo, identificacion, telefono),
            )
            return cur.lastrowid
    finally:
        conn.close()

def obtener_usuarios(ids) -> dict:
    ids = list({i for i in ids if i is not None})
    if not ids:
        return {}

    marcadores = ", ".join(["%s"] * len(ids))
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                f"""SELECT id, tipo, cargo_personal, nombre_completo,
                           correo_institucional, telefono
                    FROM usuarios WHERE id IN ({marcadores})""",
                ids,
            )
            return {fila["id"]: fila for fila in cur.fetchall()}
    finally:
        conn.close()

def buscar_usuario_id_por_correo(correo: str):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id FROM usuarios WHERE correo_institucional = %s",
                (correo,),
            )
            fila = cur.fetchone()
            return fila["id"] if fila else None
    finally:
        conn.close()