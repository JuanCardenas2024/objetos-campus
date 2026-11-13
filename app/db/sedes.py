from app.db.mariadb import get_connection


def listar_sedes() -> list[dict]:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT nombre, departamento FROM sedes ORDER BY departamento, nombre"
            )
            return cur.fetchall()
    finally:
        conn.close()