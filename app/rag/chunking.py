"""Partir texto en fragmentos (chunks) con traslape."""
import re


def partir_texto(texto: str, tamano: int = 700, traslape: int = 120) -> list[str]:
    """Parte `texto` en chunks de ~`tamano` caracteres, cortando en límites de oración
    y repitiendo ~`traslape` caracteres del final del chunk anterior al inicio del siguiente."""
    texto = re.sub(r"\s+", " ", texto).strip()
    if not texto:
        return []
    oraciones = re.split(r"(?<=[.!?:])\s+", texto)
    chunks, actual = [], ""
    for o in oraciones:
        if actual and len(actual) + len(o) + 1 > tamano:
            chunks.append(actual)
            cola = actual[-traslape:]
            # empezar el siguiente chunk en una palabra completa
            cola = cola[cola.find(" ") + 1:] if " " in cola else ""
            actual = (cola + " " + o).strip()
        else:
            actual = (actual + " " + o).strip()
    if actual:
        chunks.append(actual)
    return chunks
