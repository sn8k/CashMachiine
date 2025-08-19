"""Database helpers v0.1.0 (2025-08-19)"""
from config import settings
import psycopg2


def get_connection():
    return psycopg2.connect(
        host=settings.db_host,
        port=settings.db_port,
        dbname=settings.db_name,
        user=settings.db_user,
        password=settings.db_pass,
    )
