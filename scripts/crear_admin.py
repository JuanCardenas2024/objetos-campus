import getpass
from argon2 import PasswordHasher
from app.db.mariadb import get_connection


def main():
    usuario = input("Usuario administrador: ").strip()
    password = getpass.getpass("Contraseña (mínimo 8 caracteres): ")

    if len(password) < 8:
        print("La contraseña debe tener mínimo 8 caracteres.")
        return

    hash_password = PasswordHasher().hash(password)

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO administradores (usuario, password_hash) VALUES (%s, %s)",
                (usuario, hash_password),
            )
        print("Administrador creado:", usuario)
    except Exception as e:
        print("No se pudo crear:", e)
    finally:
        conn.close()


if __name__ == "__main__":
    main()