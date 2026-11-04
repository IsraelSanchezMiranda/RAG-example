"""Ingesta: PDFs -> texto -> chunks -> embeddings -> tabla chunks (pgvector).  ► SESIÓN 2 · TODO 2"""
from pathlib import Path

from pypdf import PdfReader

from app import config, db, llm
from app.rag.chunking import partir_texto


def leer_pdf(ruta: Path) -> list[tuple[int, str]]:
    """Regresa [(número_de_página, texto), ...].  (Ya viene hecha.)"""
    return [(i, p.extract_text() or "") for i, p in enumerate(PdfReader(str(ruta)).pages, 1)]


def ingestar(carpeta: str | None = None) -> int:
    """Reemplaza el contenido de la tabla `chunks`. Regresa cuántos chunks guardó.

    TODO:
      1. Recorre los PDFs de `carpeta` (default config.DOCS_DIR) con Path.glob("*.pdf").
      2. Por cada página, usa partir_texto() y junta filas (documento, página, índice, texto).
      3. Calcula los embeddings con llm.embeddings(lista_de_textos). Hazlo en lotes de ~16.
      4. Con db.conectar(): TRUNCATE chunks y luego INSERT de cada fila.
         El vector se manda como texto con db.a_literal_vector(vec) y se castea:  %s::vector
    Prueba:  python -m scripts.ingestar   y luego:  SELECT count(*) FROM chunks;
    """
    raise NotImplementedError("TODO 2: implementa ingestar")
