"""Orquestador del asistente.

PASO 1: el asistente solo le pasa tu pregunta al LLM. NO tiene acceso a la base de datos
ni a los documentos, así que va a inventar (alucinar) las respuestas sobre la empresa.
Pruébalo: "¿Cuáles son las ventas totales por sucursal?" y compara con la base real.
En los siguientes pasos le vamos dando acceso a los documentos (RAG) y a los datos (SQL).
"""
from app import llm

SISTEMA = ("Eres el asistente de datos de Distribuidora del Bajío. Responde en español, breve y preciso.")


def responder(pregunta: str) -> dict:
    texto = llm.chat([{"role": "system", "content": SISTEMA},
                      {"role": "user", "content": pregunta}])
    return {"respuesta": texto, "ruta": "solo_llm", "sql": None, "fuentes": []}
