from app.rag.chunking import partir_texto


def test_vacio():
    assert partir_texto("   ") == []


def test_texto_corto_un_chunk():
    assert partir_texto("Hola mundo.") == ["Hola mundo."]


def test_respeta_tamano_y_traslapa():
    texto = " ".join(f"Esta es la oración número {i}." for i in range(60))
    chunks = partir_texto(texto, tamano=200, traslape=50)
    assert len(chunks) > 3
    assert all(len(c) <= 260 for c in chunks)
    # el inicio de cada chunk repite algo del final del anterior
    assert chunks[1].split()[0] in chunks[0]
