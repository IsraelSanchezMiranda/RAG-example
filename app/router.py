"""Router: decide si la pregunta va a SQL, a documentos, a ambos o es de otro tema.  ► SESIÓN 3 · TODO 5"""
import json

from app import llm

RUTAS = {"sql", "documentos", "ambos", "fuera_de_tema"}

PROMPT = ""  # TODO 5a: escribe el prompt del clasificador (describe cada ruta + 3 o 4 ejemplos)


def clasificar(pregunta: str) -> str:
    """Regresa una de RUTAS.

    TODO 5b: llama llm.chat(..., json_mode=True) pidiendo {"ruta": "..."}; parsea con json.loads.
    Si el JSON no sale bien o la ruta no es válida, regresa "ambos" (ante la duda, buscar en las dos fuentes).
    """
    return "ambos"
