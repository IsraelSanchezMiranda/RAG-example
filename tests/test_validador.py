import pytest

from app.sql.validador import SQLNoPermitido, validar


def test_select_ok_agrega_limit():
    assert "LIMIT" in validar("SELECT nombre FROM productos").upper()


def test_respeta_limit_existente():
    assert validar("SELECT nombre FROM productos LIMIT 5").upper().count("LIMIT") == 1


def test_join_y_cte_ok():
    validar("WITH t AS (SELECT * FROM ventas) SELECT count(*) FROM t JOIN sucursales s ON s.id = t.sucursal_id")


@pytest.mark.parametrize("sql", [
    "DELETE FROM ventas",
    "DROP TABLE ventas",
    "UPDATE productos SET precio_unitario = 0",
    "SELECT 1; DROP TABLE ventas",
    "SELECT * FROM clientes",
    "SELECT email FROM clientes",
    "SELECT * FROM pg_user",
    "esto no es sql",
])
def test_rechazados(sql):
    with pytest.raises(SQLNoPermitido):
        validar(sql)
