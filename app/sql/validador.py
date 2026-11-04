"""Validación del SQL generado por el LLM ANTES de ejecutarlo (defensa en capas:
esto es la capa 1; el usuario de solo lectura de Postgres es la capa 2)."""
import sqlglot
from sqlglot import exp

TABLAS_PERMITIDAS = {"ventas", "detalle_venta", "productos", "sucursales", "proveedores",
                     "inventario", "clientes_publico"}
LIMITE_MAXIMO = 200


class SQLNoPermitido(Exception):
    pass


def validar(sql: str) -> str:
    """Regresa el SQL (con LIMIT garantizado) o lanza SQLNoPermitido."""
    try:
        arboles = sqlglot.parse(sql, read="postgres")
    except sqlglot.errors.ParseError as e:
        raise SQLNoPermitido(f"SQL inválido: {e}")
    arboles = [a for a in arboles if a is not None]
    if len(arboles) != 1:
        raise SQLNoPermitido("Solo se permite una sentencia.")
    arbol = arboles[0]
    if not isinstance(arbol, exp.Select):
        raise SQLNoPermitido("Solo se permiten consultas SELECT.")
    prohibidos = (exp.Insert, exp.Update, exp.Delete, exp.Drop, exp.Create, exp.Alter, exp.Command)
    if any(arbol.find(tipo) for tipo in prohibidos):
        raise SQLNoPermitido("La consulta contiene operaciones de escritura.")
    ctes = {c.alias_or_name for c in arbol.find_all(exp.CTE)}
    for t in arbol.find_all(exp.Table):
        if t.name not in TABLAS_PERMITIDAS and t.name not in ctes:
            raise SQLNoPermitido(f"Tabla no permitida: {t.name}")
    limite = arbol.args.get("limit")
    if limite is None:
        arbol = arbol.limit(LIMITE_MAXIMO)
    return arbol.sql(dialect="postgres")
