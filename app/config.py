import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    MARIADB_HOST = os.getenv("MARIADB_HOST", "localhost")
    MARIADB_PORT = int(os.getenv("MARIADB_PORT", "3306"))
    MARIADB_USER = os.getenv("MARIADB_USER", "")
    MARIADB_PASSWORD = os.getenv("MARIADB_PASSWORD", "")
    MARIADB_DB = os.getenv("MARIADB_DB", "objetos_campus")
    MONGO_URI = os.getenv("MONGO_URI", "")
    MONGO_DB = os.getenv("MONGO_DB", "objetos_campus")
    DATALAKE_PATH = os.getenv("DATALAKE_PATH", "./datalake_local")
    SECRET_KEY = os.getenv("SECRET_KEY", "")


settings = Settings()