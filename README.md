# RAG-example · Asistente de datos de una distribuidora

Mini proyecto para practicar, a escala pequeña, lo mismo que construyen en el reto: un **chat sobre Postgres** que contesta con

- **datos estructurados** (ventas, inventario…) → *texto a SQL* con una capa semántica,
- **datos no estructurados** (contratos, facturas, políticas en PDF) → *RAG* con pgvector,
- y **defensas** contra inyección de prompts y fuga de datos personales.

Todo corre **local**: Ollama con modelos pequeños, sin nube.

```
Pregunta ─► guardrails ─► router ─┬─► SQL (capa semántica → validar → Postgres solo-lectura) ─┐
                                  └─► RAG (embeddings → pgvector → fragmentos) ────────────────┴─► LLM ─► respuesta
```

## Cómo se trabaja: una rama por paso

| Rama | Qué trae |
|---|---|
| `paso-1-ambiente` | Todo corriendo: BD con datos, PDFs, API, interfaz. El chat **aún no sabe nada** de la empresa (alucina a propósito). |
| `paso-2-rag-inicio` | Punto de partida de la sesión 2: funciones del RAG con `TODO`. Los tests fallan hasta que las implementes. |
| `paso-2-rag-solucion` | RAG funcionando con citas de documentos. |
| `paso-3-sql-inicio` | Punto de partida de la sesión 3: SQL, router y guardrails con `TODO`. |
| `paso-3-sql-solucion` (= `main`) | Proyecto completo. |

```bash
git checkout paso-2-rag-inicio                    # ver el punto de partida de un paso
git diff paso-2-rag-inicio paso-2-rag-solucion    # ver qué cambia en la solución
```

## Requisitos

- ~4 GB de RAM libres. Funciona sin GPU (modelo `qwen2.5:1.5b`, ≈15 tokens/s en una laptop con CPU).
- **Ollama** y dos modelos: `qwen2.5:1.5b` (chat) y `paraphrase-multilingual` (embeddings, 768 dimensiones).

## Opción A · Con Docker

```bash
# Una vez (Ubuntu / Linux Mint):
#   sudo apt install docker.io docker-compose-v2 && sudo usermod -aG docker $USER   (y reinicia sesión)
cp .env.example .env
ollama pull qwen2.5:1.5b && ollama pull paraphrase-multilingual
docker compose up --build
```

- Interfaz: <http://localhost:8501> · API: <http://localhost:8000/docs>
- En Linux, el contenedor llega al Ollama de tu máquina por `host.docker.internal`; para eso Ollama debe
  escuchar en todas las interfaces: `sudo systemctl edit ollama`, agrega
  `[Service]` y `Environment="OLLAMA_HOST=0.0.0.0"`, y luego `sudo systemctl restart ollama`.
- ¿Prefieres Ollama también en contenedor? `docker compose --profile ollama up --build` con
  `OLLAMA_URL=http://ollama:11434` en el entorno; los modelos se bajan con
  `docker compose exec ollama ollama pull qwen2.5:1.5b` (y el de embeddings).
- Los scripts de `db/` solo corren la primera vez. Para reiniciar la BD: `docker compose down -v`.

## Opción B · Sin Docker

```bash
bash scripts/instalar_sin_docker.sh      # Postgres 16 + pgvector, venv, Ollama y modelos
source .venv/bin/activate
uvicorn app.api:app --reload             # terminal 1
streamlit run ui/streamlit_app.py        # terminal 2
```

**macOS:** `bash scripts/instalar_mac.sh` (requiere [Homebrew](https://brew.sh)); lo demás es igual.
**Windows:** `powershell -ExecutionPolicy Bypass -File scripts\instalar_windows.ps1` instala Ubuntu en WSL2 y corre ahí el instalador de Linux.
Si en Windows o Mac prefieres lo más sencillo, usa la **Opción A (Docker Desktop)**.

## Verificar que todo funciona

```bash
python -m scripts.verificar_ambiente     # con Docker: docker compose exec api python -m scripts.verificar_ambiente
```

## Estructura

```
db/            esquema, datos y usuario de solo lectura (se cargan solos)
datos/         generadores de datos y de PDFs (reproducibles) + datos/documentos/*.pdf
app/           llm.py (Ollama) · api.py · asistente.py · rag/ · sql/ · router.py · guardrails.py
ui/            interfaz Streamlit
scripts/       verificar_ambiente.py · instalar_sin_docker.sh · ingestar.py
tests/         pruebas con pytest
```

## Los datos son ficticios

"Distribuidora del Bajío" y sus proveedores, clientes, correos y teléfonos son inventados. `clientes`
contiene datos personales y **el asistente no puede leerla**: usa la vista `clientes_publico` y un
usuario de Postgres de solo lectura.

Uno de los PDFs (`nota_aclaratoria_hidraulica_manantial.pdf`) trae una instrucción maliciosa oculta
(texto blanco) a propósito: es el ejemplo de *inyección indirecta* de la sesión 3.

## Problemas comunes

| Síntoma | Causa y solución |
|---|---|
| `connection refused` a Ollama desde Docker | Ollama escucha solo en `127.0.0.1`. Ver la nota de `OLLAMA_HOST=0.0.0.0` arriba. |
| `model not found` | Falta `ollama pull` del modelo (revisa `/salud`). |
| `type "vector" does not exist` | Falta pgvector: `sudo apt install postgresql-16-pgvector` y vuelve a crear la BD. |
| `expected 768 dimensions` | El modelo de embeddings da otra dimensión que `vector(768)`. Usa `paraphrase-multilingual` o cambia la tabla. |
| Todo muy lento | Cierra el navegador y otras apps; el modelo de 1.5 B cabe en ~2 GB. |
| Puerto 5432 ocupado | Ya tienes un Postgres local: páralo (`sudo systemctl stop postgresql`) o cambia el puerto en `docker-compose.yml`. |
