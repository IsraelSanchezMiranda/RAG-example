"""Texto -> SQL con el LLM, apoyado en la capa semántica.  ► SESIÓN 3 · TODO 2"""
import re
from pathlib import Path

import yaml

from app import llm

_RUTA = Path(__file__).with_name("capa_semantica.yaml")


def cargar_capa() -> dict:
    return yaml.safe_load(_RUTA.read_text(encoding="utf-8"))


def construir_prompt(capa: dict) -> str:
    """Convierte el YAML en el texto (system prompt) que ve el LLM.

    TODO 2: arma un texto con
      - la instrucción: "Eres experto en PostgreSQL. Responde SOLO con un SELECT, sin explicaciones."
      - TABLAS con sus columnas y descripciones   (capa["tablas"])
      - RELACIONES (los JOIN posibles)            (capa["relaciones"])
      - MÉTRICAS, SINÓNIMOS y EJEMPLOS pregunta/sql
      - reglas: solo SELECT, solo tablas listadas, usa LIMIT.
    Un modelo de 1.5 B es chico: prompt corto y claro > prompt largo.
    """
    raise NotImplementedError("TODO 2: implementa construir_prompt")


def limpiar_sql(texto: str) -> str:
    """Quita ```sql ... ``` y el punto y coma final que suelen agregar los LLM.  (Ya viene hecha.)"""
    m = re.search(r"```(?:sql)?\s*(.*?)```", texto, re.S | re.I)
    return (m.group(1) if m else texto).strip().rstrip(";").strip()


def generar_sql(pregunta: str, error_previo: str | None = None, sql_previo: str | None = None) -> str:
    """Pregunta -> SQL.  Con error_previo, le muestra al LLM su fallo para que se autocorrija.  (Ya viene hecha.)"""
    mensajes = [{"role": "system", "content": construir_prompt(cargar_capa())},
                {"role": "user", "content": pregunta}]
    if error_previo:
        mensajes += [{"role": "assistant", "content": sql_previo or ""},
                     {"role": "user", "content": f"Esa consulta falló: {error_previo}. Corrígela y responde solo con el SQL."}]
    return limpiar_sql(llm.chat(mensajes, temperatura=0.0))
