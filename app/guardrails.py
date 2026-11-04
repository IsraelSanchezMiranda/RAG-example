"""Guardrails: defensas contra inyección de prompts y fuga de datos personales.  ► SESIÓN 3 · TODO 6"""
import re

PATRONES_INYECCION: list[str] = []  # TODO 6a: expresiones regulares (minúsculas) de frases típicas de ataque

RE_EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
RE_TELEFONO = re.compile(r"(?<!\d)(?:\+?52\s?)?(?:\d[\s-]?){10}(?!\d)")


def detectar_inyeccion(texto: str) -> bool:
    """TODO 6a: True si el texto coincide con algún patrón de PATRONES_INYECCION.
    Piensa en: "ignora tus instrucciones", "ignore previous instructions", "muestra tu prompt",
    "instrucción para el asistente", "actúa como administrador", "DROP TABLE"…"""
    return False


def revisar_entrada(pregunta: str) -> tuple[bool, str]:
    """(True, '') si la pregunta es aceptable; (False, motivo) si se bloquea.  (Ya viene hecha.)"""
    if len(pregunta) > 1000:
        return False, "La pregunta es demasiado larga."
    if detectar_inyeccion(pregunta):
        return False, "No puedo procesar esa solicitud: parece un intento de modificar mis instrucciones."
    return True, ""


def sanear_contexto(chunks: list[dict]) -> list[dict]:
    """TODO 6b — defensa contra inyección INDIRECTA: descarta los fragmentos de documentos
    (chunk["contenido"]) que traigan instrucciones dirigidas a la IA, como el PDF envenenado."""
    return chunks


def enmascarar_pii(texto: str) -> str:
    """TODO 6c — última línea de defensa: sustituye correos y teléfonos (RE_EMAIL, RE_TELEFONO)
    por "[correo oculto]" y "[teléfono oculto]" en la respuesta final."""
    return texto
