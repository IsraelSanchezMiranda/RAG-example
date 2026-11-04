"""Ejecuta SQL validado con el usuario de solo lectura.  ► SESIÓN 3 · TODO 4"""
import psycopg

from app import db
from app.sql import generador, validador


def ejecutar(sql: str) -> list[dict]:
    """Corre el SQL con el usuario asistente_lectura.  (Ya viene hecha.)"""
    with db.conectar(lectura=True) as con:
        return con.execute(sql).fetchall()


def filas_a_texto(filas: list[dict], maximo: int = 30) -> str:
    """Tabla en texto plano para dársela al LLM.  (Ya viene hecha.)"""
    if not filas:
        return "(sin resultados)"
    cols = list(filas[0].keys())
    lineas = [" | ".join(cols)]
    lineas += [" | ".join(str(f[c]) for c in cols) for f in filas[:maximo]]
    if len(filas) > maximo:
        lineas.append(f"... ({len(filas) - maximo} filas más)")
    return "\n".join(lineas)


def consultar(pregunta: str, reintentos: int = 1) -> dict:
    """Pregunta -> SQL -> validar -> ejecutar. Regresa {"sql", "filas"} o {"sql", "filas": [], "error"}.

    TODO 4:
      1. sql = generador.generar_sql(pregunta)
      2. Intenta validador.validar(sql) y ejecutar(sql_validado).
      3. Si falla (validador.SQLNoPermitido o psycopg.Error), repite hasta `reintentos` veces
         pasándole al generador error_previo=<mensaje> y sql_previo=<sql fallido> (autocorrección).
      4. Si sigue fallando, regresa el error en lugar de lanzar la excepción.
    """
    raise NotImplementedError("TODO 4: implementa consultar")
