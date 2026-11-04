#!/usr/bin/env bash
# Instala y prepara todo SIN Docker en Ubuntu / Linux Mint 22 (Ubuntu 24.04).
# Uso: bash scripts/instalar_sin_docker.sh
set -euo pipefail
cd "$(dirname "$0")/.."

echo "==> 1/5 Postgres 16 + pgvector (pide tu contraseña de sudo)"
sudo apt update
sudo apt install -y postgresql postgresql-16-pgvector python3-venv python3-pip curl
sudo systemctl enable --now postgresql 2>/dev/null || sudo service postgresql start

echo "==> 2/5 Base de datos"
if sudo -u postgres psql -tAc "SELECT 1 FROM pg_database WHERE datname='distribuidora'" | grep -q 1; then
  echo "    (ya existe 'distribuidora'; para empezar de cero: sudo -u postgres dropdb distribuidora)"
else
  sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'postgres';"
  sudo -u postgres createdb distribuidora
  for f in db/01_esquema.sql db/02_datos.sql db/03_usuario_lectura.sql; do
    # se lee con "<" para que el archivo lo abra TU usuario (postgres no puede entrar a tu carpeta personal)
    sudo -u postgres psql -v ON_ERROR_STOP=1 -q -d distribuidora < "$f"
  done
fi

echo "==> 3/5 Entorno de Python"
python3 -m venv .venv
.venv/bin/pip install -q -r requirements.txt
[ -f .env ] || cp .env.example .env

echo "==> 4/5 Ollama y modelos"
command -v ollama >/dev/null || curl -fsSL https://ollama.com/install.sh | sh
if ! curl -s http://localhost:11434 >/dev/null; then   # p. ej. WSL sin systemd
  (nohup ollama serve >/tmp/ollama.log 2>&1 &)
  for _ in $(seq 1 30); do curl -s http://localhost:11434 >/dev/null && break; sleep 1; done
fi
ollama pull qwen2.5:1.5b
ollama pull paraphrase-multilingual

echo "==> 5/5 Listo. Ahora:"
echo "    source .venv/bin/activate && python -m scripts.verificar_ambiente"
