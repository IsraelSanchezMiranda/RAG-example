"""Revisa que todo esté listo. Uso: python -m scripts.verificar_ambiente"""
import sys

import psycopg

from app import config, db, llm

fallos = 0


def paso(nombre, fn):
    global fallos
    try:
        print(f"  ✅ {nombre}: {fn()}")
    except Exception as e:
        fallos += 1
        print(f"  ❌ {nombre}: {str(e).splitlines()[0] if str(e) else type(e).__name__}")


def postgres():
    with db.conectar() as con:
        n = con.execute("SELECT count(*) AS n FROM ventas").fetchone()["n"]
        v = con.execute("SELECT extname FROM pg_extension WHERE extname='vector'").fetchone()
    assert v, "falta la extensión pgvector"
    return f"{n} ventas, pgvector instalado"


def lectura():
    with db.conectar(lectura=True) as con:
        con.execute("SELECT count(*) FROM clientes_publico").fetchone()
        try:
            con.execute("SELECT email FROM clientes")
        except psycopg.errors.InsufficientPrivilege:
            return "puede leer clientes_publico y NO puede leer clientes"
    raise AssertionError("¡el usuario de lectura puede leer la tabla clientes!")


def modelos():
    inst = [m.split(":")[0] for m in llm.modelos_instalados()]
    faltan = [m for m in (config.LLM_MODEL, config.EMBED_MODEL) if m.split(":")[0] not in inst]
    assert not faltan, f"faltan modelos, corre: ollama pull {' '.join(faltan)}"
    return "ok"


def generar():
    return llm.chat([{"role": "user", "content": "Responde solo: listo"}]).strip()[:40]


def embed():
    v = llm.embeddings(["hola"])[0]
    assert len(v) == config.EMBED_DIM, f"el modelo da {len(v)} dimensiones y la tabla espera {config.EMBED_DIM}"
    return f"{len(v)} dimensiones"


print("Verificando ambiente…")
paso("Postgres + datos + pgvector", postgres)
paso("Usuario de solo lectura", lectura)
paso("Ollama: modelos instalados", modelos)
paso("Ollama: generación", generar)
paso("Ollama: embeddings", embed)
print("\nTodo listo 🎉" if not fallos else f"\n{fallos} problema(s). Revisa el README, sección 'Problemas comunes'.")
sys.exit(1 if fallos else 0)
