"""Acceso a Postgres. Dos conexiones con permisos distintos (idea clave de seguridad):
- admin: para ingestar los chunks (escritura).
- lectura: usuario asistente_lectura, el ÚNICO que ejecuta SQL generado por el LLM."""
import psycopg
from psycopg.rows import dict_row

from app import config


def conectar(lectura: bool = False):
    url = config.DATABASE_URL_LECTURA if lectura else config.DATABASE_URL
    return psycopg.connect(url, row_factory=dict_row)


def a_literal_vector(v: list[float]) -> str:
    """pgvector acepta '[0.1,0.2,...]' como texto; se le hace ::vector en la consulta."""
    return "[" + ",".join(f"{x:.6f}" for x in v) + "]"
