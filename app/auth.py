from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from app.db.mariadb import get_connection

ph = PasswordHasher()


def verificar_admin(usuario: str, password: str) -> bool:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT password_hash FROM administradores WHERE usuario = %s",
                (usuario,),
            )
            fila = cur.fetchone()
    finally:
        conn.close()

    if not fila:
        return False
    try:
        return ph.verify(fila["password_hash"], password)
    except VerifyMismatchError:
        return False