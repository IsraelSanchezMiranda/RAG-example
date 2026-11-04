"""Uso: python -m scripts.ingestar   (desde la raíz del repo)"""
from app.rag.ingesta import ingestar

if __name__ == "__main__":
    print(f"Listo: {ingestar()} chunks guardados.")
