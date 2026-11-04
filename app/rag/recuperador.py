"""Búsqueda semántica en pgvector.  ► SESIÓN 2 · TODO 3"""
from app import db, llm


def buscar(pregunta: str, k: int = 4) -> list[dict]:
    """Los k chunks más parecidos a la pregunta. Cada dict: documento, pagina, contenido, similitud.

    TODO:
      1. Convierte la pregunta en vector: llm.embeddings([pregunta])[0].
      2. Consulta con el operador de distancia coseno de pgvector:
             SELECT ..., 1 - (embedding <=> %s::vector) AS similitud
             FROM chunks ORDER BY embedding <=> %s::vector LIMIT %s
      3. Regresa las filas (con db.conectar(), las filas ya son diccionarios).
    """
    raise NotImplementedError("TODO 3: implementa buscar")
