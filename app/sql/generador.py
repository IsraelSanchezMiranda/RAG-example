"""Texto -> SQL con el LLM, apoyado en la capa semántica."""
import re
from pathlib import Path

import yaml

from app import llm

_RUTA = Path(__file__).with_name("capa_semantica.yaml")


def cargar_capa() -> dict:
    return yaml.safe_load(_RUTA.read_text(encoding="utf-8"))


def construir_prompt(capa: dict) -> str:
    """Convierte el YAML en el texto que ve el LLM (lo único que sabe de tu negocio)."""
    lineas = ["Eres un experto en PostgreSQL. Responde SOLO con una consulta SQL (un solo SELECT), sin explicaciones.",
              "", "TABLAS:"]
    for t, info in capa["tablas"].items():
        lineas.append(f"- {t}: {info['descripcion']}")
        for c, d in info["columnas"].items():
            lineas.append(f"    {t}.{c}: {d}")
    lineas += ["", "RELACIONES:"] + [f"- {r}" for r in capa["relaciones"]]
    lineas += ["", "MÉTRICAS:"] + [f"- {k} = {v}" for k, v in capa["metricas"].items()]
    lineas += ["", "SINÓNIMOS:"] + [f"- {k} -> {v}" for k, v in capa["sinonimos"].items()]
    lineas += ["", "EJEMPLOS:"]
    for e in capa["ejemplos"]:
        lineas += [f"Pregunta: {e['pregunta']}", f"SQL: {' '.join(e['sql'].split())}"]
    lineas += ["", "Reglas: solo SELECT; usa solo las tablas listadas; agrega LIMIT cuando devuelvas filas sueltas."]
    return "\n".join(lineas)


def limpiar_sql(texto: str) -> str:
    """Quita ```sql ... ``` y el punto y coma final que suelen agregar los LLM."""
    m = re.search(r"```(?:sql)?\s*(.*?)```", texto, re.S | re.I)
    return (m.group(1) if m else texto).strip().rstrip(";").strip()


def generar_sql(pregunta: str, error_previo: str | None = None, sql_previo: str | None = None) -> str:
    mensajes = [{"role": "system", "content": construir_prompt(cargar_capa())},
                {"role": "user", "content": pregunta}]
    if error_previo:  # autocorrección: se le muestra su error y se le pide otra versión
        mensajes += [{"role": "assistant", "content": sql_previo or ""},
                     {"role": "user", "content": f"Esa consulta falló: {error_previo}. Corrígela y responde solo con el SQL."}]
    return limpiar_sql(llm.chat(mensajes, temperatura=0.0))
