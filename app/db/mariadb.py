import pymysql
from app.config import settings


def get_connection():
    return pymysql.connect(
        host=settings.MARIADB_HOST,
        port=settings.MARIADB_PORT,
        user=settings.MARIADB_USER,
        password=settings.MARIADB_PASSWORD,
        database=settings.MARIADB_DB,
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True,
    )