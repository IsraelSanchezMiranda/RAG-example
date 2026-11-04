-- Usuario de SOLO LECTURA que usa el asistente para ejecutar SQL generado por el LLM.
-- Idea clave: aunque el LLM se equivoque o lo manipulen, la base de datos no lo deja
-- modificar datos ni leer datos personales.
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'asistente_lectura') THEN
        CREATE ROLE asistente_lectura WITH LOGIN PASSWORD 'lectura123';
    END IF;
END $$;
GRANT CONNECT ON DATABASE distribuidora TO asistente_lectura;
GRANT USAGE ON SCHEMA public TO asistente_lectura;
GRANT SELECT ON sucursales, proveedores, productos, ventas, detalle_venta,
                inventario, clientes_publico TO asistente_lectura;
REVOKE ALL ON clientes FROM asistente_lectura;
ALTER ROLE asistente_lectura SET statement_timeout = '10s';
