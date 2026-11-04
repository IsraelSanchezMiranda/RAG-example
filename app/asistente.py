"""Orquestador del asistente.

PASO 2: RAG. Busca fragmentos de los PDFs parecidos a la pregunta y se los da al LLM como contexto.
Aún NO hay SQL (no sabe de ventas ni inventario) ni defensas (¡prueba preguntar por Hidráulica Manantial!).
"""
from app import llm
from app.rag import recuperador

SISTEMA = ("Eres el asistente de datos de Distribuidora del Bajío. Responde en español, breve y preciso, "
           "usando SOLO el contexto dado. Si el contexto no alcanza, di que no tienes esa información.")


def responder(pregunta: str) -> dict:
    chunks = recuperador.buscar(pregunta)
    fuentes = sorted({f"{c['documento']} (p. {c['pagina']})" for c in chunks})
    contexto = "\n---\n".join(f"[{c['documento']}] {c['contenido']}" for c in chunks) or "(sin documentos relevantes)"
    texto = llm.chat([{"role": "system", "content": SISTEMA},
                      {"role": "user", "content": f"FRAGMENTOS DE DOCUMENTOS:\n{contexto}\n\nPREGUNTA: {pregunta}"}])
    return {"respuesta": texto, "ruta": "documentos", "sql": None, "fuentes": fuentes}
