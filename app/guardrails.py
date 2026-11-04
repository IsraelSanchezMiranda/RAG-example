"""Guardrails: defensas contra inyección de prompts y fuga de datos personales."""
import re

PATRONES_INYECCION = [
    r"ignor[ae]\s+(todas?\s+)?(tus|las|mis)?\s*(instrucciones|reglas|indicaciones)",
    r"olvida\s+(todas?\s+)?(tus|las)?\s*(instrucciones|reglas)",
    r"ignore\s+(all\s+)?(previous|prior|your)\s+instructions",
    r"(muestra|dame|revela|imprime)\s+(tu|el)\s+(prompt|system prompt|mensaje del sistema)",
    r"act[uú]a\s+como\s+(si\s+fueras\s+)?(administrador|root|dan)",
    r"instrucci[oó]n\s+para\s+el\s+asistente",
    r"\b(drop|truncate)\s+table|\bdelete\s+from|\binsert\s+into",
]

RE_EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
RE_TELEFONO = re.compile(r"(?<!\d)(?:\+?52\s?)?(?:\d[\s-]?){10}(?!\d)")


def detectar_inyeccion(texto: str) -> bool:
    t = texto.lower()
    return any(re.search(p, t) for p in PATRONES_INYECCION)


def revisar_entrada(pregunta: str) -> tuple[bool, str]:
    """(True, '') si la pregunta es aceptable; (False, motivo) si se bloquea."""
    if len(pregunta) > 1000:
        return False, "La pregunta es demasiado larga."
    if detectar_inyeccion(pregunta):
        return False, "No puedo procesar esa solicitud: parece un intento de modificar mis instrucciones."
    return True, ""


def sanear_contexto(chunks: list[dict]) -> list[dict]:
    """Defensa contra inyección INDIRECTA: descarta los fragmentos de documentos que traen
    instrucciones dirigidas a la IA (como el PDF envenenado de datos/documentos)."""
    return [c for c in chunks if not detectar_inyeccion(c["contenido"])]


def enmascarar_pii(texto: str) -> str:
    """Última línea de defensa: aunque algo se cuele, no sale ningún correo ni teléfono."""
    texto = RE_EMAIL.sub("[correo oculto]", texto)
    return RE_TELEFONO.sub("[teléfono oculto]", texto)
