#!/usr/bin/env bash
# Instala y prepara todo SIN Docker en macOS (Apple Silicon o Intel) con Homebrew.
# Uso: bash scripts/instalar_mac.sh
set -euo pipefail
cd "$(dirname "$0")/.."

command -v brew >/dev/null || { echo "Falta Homebrew. Instálalo desde https://brew.sh y vuelve a correr este script."; exit 1; }

echo "==> 1/5 Postgres + pgvector"
brew install postgresql@17 pgvector
brew services start postgresql@17
export PATH="$(brew --prefix postgresql@17)/bin:$PATH"
for _ in $(seq 1 30); do pg_isready -q && break; sleep 1; done
pg_isready -q || { echo "Postgres no arrancó. Revisa: brew services list"; exit 1; }

echo "==> 2/5 Base de datos"
# En Homebrew el superusuario es tu usuario de macOS; se crea 'postgres' para que coincida con el .env
psql -d postgres -tAc "SELECT 1 FROM pg_roles WHERE rolname='postgres'" | grep -q 1 \
  || psql -d postgres -c "CREATE ROLE postgres WITH SUPERUSER LOGIN PASSWORD 'postgres';"
if psql -d postgres -tAc "SELECT 1 FROM pg_database WHERE datname='distribuidora'" | grep -q 1; then
  echo "    (ya existe 'distribuidora'; para empezar de cero: dropdb distribuidora)"
else
  createdb distribuidora
  for f in db/01_esquema.sql db/02_datos.sql db/03_usuario_lectura.sql; do
    psql -v ON_ERROR_STOP=1 -q -d distribuidora -f "$f" \
      || { echo "Falló $f. Si dice que no existe la extensión 'vector', corre: brew reinstall pgvector"; exit 1; }
  done
fi

echo "==> 3/5 Entorno de Python"
command -v python3 >/dev/null || brew install python
python3 -m venv .venv
.venv/bin/pip install -q -r requirements.txt
[ -f .env ] || cp .env.example .env

echo "==> 4/5 Ollama y modelos"
command -v ollama >/dev/null || brew install ollama
if ! curl -s http://localhost:11434 >/dev/null; then
  brew services start ollama 2>/dev/null || open -a Ollama 2>/dev/null || true
  for _ in $(seq 1 30); do curl -s http://localhost:11434 >/dev/null && break; sleep 1; done
fi
ollama pull qwen2.5:1.5b
ollama pull paraphrase-multilingual

echo "==> 5/5 Listo. Ahora:"
echo "    source .venv/bin/activate && python -m scripts.verificar_ambiente"
