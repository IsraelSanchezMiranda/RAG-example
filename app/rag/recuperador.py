"""Búsqueda semántica en pgvector."""
from app import db, llm


def buscar(pregunta: str, k: int = 4) -> list[dict]:
    """Los k chunks más cercanos a la pregunta (distancia coseno, operador <=>)."""
    vec = llm.embeddings([pregunta])[0]
    with db.conectar() as con:
        return con.execute(
            "SELECT documento, pagina, contenido, 1 - (embedding <=> %s::vector) AS similitud "
            "FROM chunks ORDER BY embedding <=> %s::vector LIMIT %s",
            (db.a_literal_vector(vec),) * 2 + (k,)).fetchall()
