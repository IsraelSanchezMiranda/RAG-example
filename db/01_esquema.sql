-- Esquema de la distribuidora ficticia "Distribuidora del Bajío".
-- Se ejecuta automáticamente al crear el contenedor de Postgres (Docker)
-- o con scripts/instalar_sin_docker.sh (sin Docker).

CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE sucursales (
    id      SERIAL PRIMARY KEY,
    nombre  TEXT NOT NULL,
    ciudad  TEXT NOT NULL
);

CREATE TABLE proveedores (
    id        SERIAL PRIMARY KEY,
    nombre    TEXT NOT NULL,
    rfc       TEXT NOT NULL,
    ciudad    TEXT NOT NULL,
    contacto  TEXT NOT NULL
);

CREATE TABLE productos (
    id               SERIAL PRIMARY KEY,
    sku              TEXT NOT NULL UNIQUE,
    nombre           TEXT NOT NULL,
    categoria        TEXT NOT NULL,
    proveedor_id     INT  NOT NULL REFERENCES proveedores(id),
    precio_unitario  NUMERIC(10,2) NOT NULL,
    costo_unitario   NUMERIC(10,2) NOT NULL
);

-- Contiene datos personales (email, teléfono): el asistente NO debe leerla.
CREATE TABLE clientes (
    id              SERIAL PRIMARY KEY,
    nombre          TEXT NOT NULL,
    tipo            TEXT NOT NULL CHECK (tipo IN ('empresa', 'persona')),
    ciudad          TEXT NOT NULL,
    email           TEXT NOT NULL,
    telefono        TEXT NOT NULL,
    fecha_alta      DATE NOT NULL,
    limite_credito  NUMERIC(12,2) NOT NULL
);

-- Vista sin datos personales: es lo único de clientes que ve el asistente.
CREATE VIEW clientes_publico AS
    SELECT id, nombre, tipo, ciudad, fecha_alta, limite_credito FROM clientes;

CREATE TABLE ventas (
    id           SERIAL PRIMARY KEY,
    fecha        DATE NOT NULL,
    cliente_id   INT  NOT NULL REFERENCES clientes(id),
    sucursal_id  INT  NOT NULL REFERENCES sucursales(id),
    metodo_pago  TEXT NOT NULL
);

CREATE TABLE detalle_venta (
    id               SERIAL PRIMARY KEY,
    venta_id         INT NOT NULL REFERENCES ventas(id),
    producto_id      INT NOT NULL REFERENCES productos(id),
    cantidad         INT NOT NULL,
    precio_unitario  NUMERIC(10,2) NOT NULL
);

CREATE TABLE inventario (
    producto_id  INT NOT NULL REFERENCES productos(id),
    sucursal_id  INT NOT NULL REFERENCES sucursales(id),
    existencias  INT NOT NULL,
    PRIMARY KEY (producto_id, sucursal_id)
);

-- Para el RAG (sesión 2): fragmentos de los PDFs con su embedding.
-- 768 dimensiones = modelo paraphrase-multilingual de Ollama.
CREATE TABLE chunks (
    id         SERIAL PRIMARY KEY,
    documento  TEXT NOT NULL,
    pagina     INT  NOT NULL,
    indice     INT  NOT NULL,
    contenido  TEXT NOT NULL,
    embedding  vector(768)
);
CREATE INDEX chunks_embedding_idx ON chunks USING hnsw (embedding vector_cosine_ops);
