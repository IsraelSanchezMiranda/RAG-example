"""Configuración leída de variables de entorno (ver .env.example)."""
import os
from pathlib import Path


def _cargar_env():
    """Lee el archivo .env de la raíz del repo (si existe) SIN pisar variables ya definidas
    (así, dentro de Docker mandan las del docker-compose)."""
    ruta = Path(__file__).resolve().parent.parent / ".env"
    if ruta.exists():
        for linea in ruta.read_text(encoding="utf-8").splitlines():
            linea = linea.strip()
            if linea and not linea.startswith("#") and "=" in linea:
                k, v = linea.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())


_cargar_env()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/distribuidora")
DATABASE_URL_LECTURA = os.getenv(
    "DATABASE_URL_LECTURA", "postgresql://asistente_lectura:lectura123@localhost:5432/distribuidora")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
LLM_MODEL = os.getenv("LLM_MODEL", "qwen2.5:1.5b")
EMBED_MODEL = os.getenv("EMBED_MODEL", "paraphrase-multilingual")
EMBED_DIM = int(os.getenv("EMBED_DIM", "768"))
API_URL = os.getenv("API_URL", "http://localhost:8000")
DOCS_DIR = os.getenv("DOCS_DIR", "datos/documentos")
