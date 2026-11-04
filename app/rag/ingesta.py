"""Ingesta: PDFs -> texto -> chunks -> embeddings -> tabla chunks (pgvector)."""
from pathlib import Path

from pypdf import PdfReader

from app import config, db, llm
from app.rag.chunking import partir_texto


def leer_pdf(ruta: Path) -> list[tuple[int, str]]:
    """Regresa [(número_de_página, texto), ...]."""
    return [(i, p.extract_text() or "") for i, p in enumerate(PdfReader(str(ruta)).pages, 1)]


def ingestar(carpeta: str | None = None) -> int:
    """Reemplaza el contenido de `chunks`. Regresa cuántos chunks guardó."""
    carpeta = Path(carpeta or config.DOCS_DIR)
    filas = []
    for pdf in sorted(carpeta.glob("*.pdf")):
        indice = 0
        for pagina, texto in leer_pdf(pdf):
            for trozo in partir_texto(texto):
                filas.append((pdf.name, pagina, indice, trozo))
                indice += 1
    vectores = []
    for i in range(0, len(filas), 16):  # lotes pequeños: la laptop lo agradece
        vectores += llm.embeddings([f[3] for f in filas[i:i + 16]])
    with db.conectar() as con:
        con.execute("TRUNCATE chunks RESTART IDENTITY")
        for (doc, pag, idx, txt), vec in zip(filas, vectores):
            con.execute(
                "INSERT INTO chunks (documento, pagina, indice, contenido, embedding) "
                "VALUES (%s, %s, %s, %s, %s::vector)",
                (doc, pag, idx, txt, db.a_literal_vector(vec)))
    return len(filas)
