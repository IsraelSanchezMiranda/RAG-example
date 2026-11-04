"""Ejecuta SQL validado con el usuario de solo lectura y arma texto para el LLM."""
import psycopg

from app import db
from app.sql import generador, validador


def ejecutar(sql: str) -> list[dict]:
    with db.conectar(lectura=True) as con:
        return con.execute(sql).fetchall()


def consultar(pregunta: str, reintentos: int = 1) -> dict:
    """Pregunta -> SQL -> validar -> ejecutar; si falla, un reintento con el error como pista."""
    sql, error = generador.generar_sql(pregunta), None
    for intento in range(reintentos + 1):
        try:
            sql_ok = validador.validar(sql)
            return {"sql": sql_ok, "filas": ejecutar(sql_ok)}
        except (validador.SQLNoPermitido, psycopg.Error) as e:
            error = str(e).strip().splitlines()[0]
            if intento < reintentos:
                sql = generador.generar_sql(pregunta, error_previo=error, sql_previo=sql)
    return {"sql": sql, "filas": [], "error": error}


def filas_a_texto(filas: list[dict], maximo: int = 30) -> str:
    if not filas:
        return "(sin resultados)"
    cols = list(filas[0].keys())
    lineas = [" | ".join(cols)]
    lineas += [" | ".join(str(f[c]) for c in cols) for f in filas[:maximo]]
    if len(filas) > maximo:
        lineas.append(f"... ({len(filas) - maximo} filas más)")
    return "\n".join(lineas)
