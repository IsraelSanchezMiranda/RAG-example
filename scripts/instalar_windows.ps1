# Instala y prepara todo SIN Docker en Windows 10/11 usando WSL2 (Ubuntu 24.04).
# Postgres + pgvector no se instalan bien directo en Windows; dentro de WSL funciona igual que en Linux.
#
# Uso (PowerShell, desde la carpeta del repo):
#   powershell -ExecutionPolicy Bypass -File scripts\instalar_windows.ps1
$ErrorActionPreference = "Stop"
$distro = "Ubuntu-24.04"
$repo = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path

if (-not (Get-Command wsl -ErrorAction SilentlyContinue)) {
    throw "No se encontró WSL. Necesitas Windows 10 (2004 o superior) o Windows 11."
}

$instaladas = ((wsl -l -q) -join "`n") -replace "`0", ""
if ($instaladas -notmatch [regex]::Escape($distro)) {
    Write-Host "==> Instalando $distro en WSL (puede pedir permisos de administrador)..."
    wsl --install -d $distro
    Write-Host ""
    Write-Host "Cuando termine: 1) reinicia Windows si te lo pide, 2) abre 'Ubuntu 24.04' una vez y crea tu"
    Write-Host "usuario y contraseña, 3) vuelve a correr este mismo script."
    exit 0
}

Write-Host "==> Copiando el proyecto al disco de Linux (es mucho más rápido que trabajar en C:)..."
$origen = $repo -replace "\\", "/"
$cmd = "set -e; WSLREPO=`$(wslpath -a '$origen'); mkdir -p ~/RAG-example; cp -r `"`$WSLREPO/.`" ~/RAG-example/; " +
       "cd ~/RAG-example; find . -name '*.sh' -exec sed -i 's/\r$//' {} +; bash scripts/instalar_sin_docker.sh"
wsl -d $distro -- bash -lc $cmd

Write-Host ""
Write-Host "Listo. Para trabajar:"
Write-Host "  wsl -d $distro"
Write-Host "  cd ~/RAG-example && source .venv/bin/activate"
Write-Host "  python -m scripts.verificar_ambiente"
Write-Host "La interfaz se abre en el navegador de Windows: http://localhost:8501"
