"""Validación del SQL generado por el LLM ANTES de ejecutarlo.  ► SESIÓN 3 · TODO 3
Defensa en capas: esto es la capa 1; el usuario de solo lectura de Postgres es la capa 2."""
import sqlglot
from sqlglot import exp

TABLAS_PERMITIDAS = {"ventas", "detalle_venta", "productos", "sucursales", "proveedores",
                     "inventario", "clientes_publico"}
LIMITE_MAXIMO = 200


class SQLNoPermitido(Exception):
    pass


def validar(sql: str) -> str:
    """Regresa el SQL (con LIMIT garantizado) o lanza SQLNoPermitido.

    TODO 3 (usa sqlglot: sqlglot.parse(sql, read="postgres")):
      1. Si no se puede parsear -> SQLNoPermitido.
      2. Debe haber UNA sola sentencia (evita "SELECT 1; DROP TABLE ...").
      3. Debe ser un exp.Select (nada de INSERT/UPDATE/DELETE/DROP...).
      4. Cada tabla (arbol.find_all(exp.Table)) debe estar en TABLAS_PERMITIDAS
         (ojo con las CTE: WITH t AS (...) define nombres que no son tablas reales).
      5. Si no trae LIMIT, agrégale LIMIT_MAXIMO (arbol.limit(n)).
      6. Regresa arbol.sql(dialect="postgres").
    Cuando pase:  pytest tests/test_validador.py
    """
    raise NotImplementedError("TODO 3: implementa validar")
