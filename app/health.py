from pymongo.errors import PyMongoError
from app.db.mariadb import get_connection
from app.db.mongo import get_db
from app.datalake.storage import verificar_datalake


def probar_mariadb():
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT VERSION() AS v")
            version = cur.fetchone()["v"]
        conn.close()
        return True, f"OK (versión {version})"
    except Exception as e:
        return False, f"ERROR: {e}"


def probar_mongo():
    try:
        get_db().command("ping")
        return True, "OK"
    except PyMongoError as e:
        return False, f"ERROR: {e}"


def probar_datalake():
    try:
        verificar_datalake()
        return True, "OK"
    except Exception as e:
        return False, f"ERROR: {e}"


def estado_general():
    return {
        "mariadb": probar_mariadb(),
        "mongodb": probar_mongo(),
        "datalake": probar_datalake(),
    }