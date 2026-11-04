"""Orquestador del asistente.

PASO 2 (inicio): ya existe el módulo de RAG, pero el asistente todavía no lo usa.
► SESIÓN 2 · TODO 4: en responder(), busca fragmentos con recuperador.buscar(pregunta),
  arma un prompt con ese contexto, pídele al LLM que conteste SOLO con él, y regresa las fuentes.
"""
from app import llm

SISTEMA = ("Eres el asistente de datos de Distribuidora del Bajío. Responde en español, breve y preciso.")


def responder(pregunta: str) -> dict:
    # TODO 4: reemplaza esto por RAG.
    #   - chunks = recuperador.buscar(pregunta)
    #   - contexto = los chunks unidos, cada uno con el nombre de su documento
    #   - SISTEMA debe decir: "usa SOLO el contexto; si no alcanza, di que no tienes esa información"
    #   - "fuentes": lista de "documento (p. N)" sin repetir
    texto = llm.chat([{"role": "system", "content": SISTEMA},
                      {"role": "user", "content": pregunta}])
    return {"respuesta": texto, "ruta": "solo_llm", "sql": None, "fuentes": []}
