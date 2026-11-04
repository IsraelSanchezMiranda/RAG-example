"""Partir texto en fragmentos (chunks) con traslape.  ► SESIÓN 2 · TODO 1"""


def partir_texto(texto: str, tamano: int = 700, traslape: int = 120) -> list[str]:
    """Parte `texto` en chunks de ~`tamano` caracteres.

    TODO:
      1. Normaliza espacios en blanco (re.sub(r"\s+", " ", ...)).
      2. Parte el texto en oraciones (re.split con lookbehind en . ! ? :).
      3. Ve juntando oraciones hasta acercarte a `tamano`; entonces cierra el chunk.
      4. El siguiente chunk empieza repitiendo ~`traslape` caracteres del final del anterior
         (¿por qué? para que una idea cortada a la mitad aparezca completa en algún chunk).
         Cuida no empezar en medio de una palabra.
      5. Texto vacío -> [].
    Cuando pase:  pytest tests/test_chunking.py
    """
    raise NotImplementedError("TODO 1: implementa partir_texto")
