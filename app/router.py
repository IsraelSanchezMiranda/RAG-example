"""Router: decide si la pregunta se contesta con datos (SQL), documentos (RAG), ambos o ninguno."""
import json

from app import llm

RUTAS = {"sql", "documentos", "ambos", "fuera_de_tema"}

PROMPT = """Clasifica la pregunta de un usuario de una distribuidora (ferretería mayorista).
Responde SOLO un JSON: {"ruta": "<valor>"} con uno de estos valores:
- "sql": cifras o datos de la base (ventas, inventario, productos, sucursales, clientes, proveedores).
- "documentos": contratos, facturas, políticas (devoluciones, garantías, crédito, privacidad) o el manual de procedimientos.
- "ambos": necesita datos y también documentos.
- "fuera_de_tema": nada que ver con la distribuidora.
Ejemplos:
"¿Cuánto vendimos en León?" -> {"ruta": "sql"}
"¿En cuántos días se paga a Valquiria?" -> {"ruta": "documentos"}
"¿Cuánto hemos comprado a Valquiria y en qué plazo se les paga?" -> {"ruta": "ambos"}
"¿Quién ganó el mundial?" -> {"ruta": "fuera_de_tema"}"""


def clasificar(pregunta: str) -> str:
    try:
        crudo = llm.chat([{"role": "system", "content": PROMPT}, {"role": "user", "content": pregunta}],
                         json_mode=True, temperatura=0.0)
        ruta = json.loads(crudo).get("ruta", "")
    except (ValueError, KeyError):
        ruta = ""
    return ruta if ruta in RUTAS else "ambos"  # ante la duda, buscar en las dos fuentes
