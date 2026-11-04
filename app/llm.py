"""Cliente mínimo de Ollama (solo httpx; sin librerías de LLM, para ver qué pasa por debajo)."""
import httpx

from app import config

_TIMEOUT = 180.0


def chat(mensajes: list[dict], json_mode: bool = False, temperatura: float = 0.1) -> str:
    """POST /api/chat. mensajes = [{"role": "system"|"user"|"assistant", "content": "..."}]."""
    cuerpo = {"model": config.LLM_MODEL, "messages": mensajes, "stream": False,
              "options": {"temperature": temperatura}}
    if json_mode:
        cuerpo["format"] = "json"
    r = httpx.post(f"{config.OLLAMA_HOST}/api/chat", json=cuerpo, timeout=_TIMEOUT)
    r.raise_for_status()
    return r.json()["message"]["content"]


def embeddings(textos: list[str]) -> list[list[float]]:
    """POST /api/embed. Regresa un vector (lista de floats) por cada texto."""
    r = httpx.post(f"{config.OLLAMA_HOST}/api/embed",
                   json={"model": config.EMBED_MODEL, "input": textos}, timeout=_TIMEOUT)
    r.raise_for_status()
    return r.json()["embeddings"]


def modelos_instalados() -> list[str]:
    r = httpx.get(f"{config.OLLAMA_HOST}/api/tags", timeout=10)
    r.raise_for_status()
    return [m["name"] for m in r.json().get("models", [])]
