<#
  Subir el banco SERUMS a GitHub (automatizado).

  Uso:
    .\subir_serums_banco.ps1 -Token "<token>"
  O seteando la variable de entorno GITHUB_TOKEN:
    $env:GITHUB_TOKEN = "<token>"; .\subir_serums_banco.ps1

  El token necesario es un Personal Access Token clásico (classic PAT) con scope "repo":
    https://github.com/settings/tokens
#>
param(
    [string]$Token = $env:GITHUB_TOKEN,
    [string]$Repo = "serums-banco",
    [string]$Description = "Banco de preguntas SERUMS Medicina Humana - 400 preguntas (MINSA, 2025-2026)"
)

$ErrorActionPreference = "Stop"
$Base = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Base

if (-not $Token) {
    Write-Host "[WARN] Necesitás un token de acceso personal clásico (classic PAT) con scope 'repo': https://github.com/settings/tokens"
    exit 1
}

Write-Host "[INFO] Buscando tu usuario de GitHub..."
try {
    $me = Invoke-RestMethod -Uri "https://api.github.com/user" -Method Get -Headers @{ Authorization = "Bearer $Token" }
    $User = $me.login
} catch {
    Write-Host "[WARN] Token no válido o sin acceso: $($_.Exception.Message)"
    exit 1
}
Write-Host "[INFO] Usuario de GitHub: $User"

Write-Host "[INFO] Creando o verificando el repo $User/$Repo ..."
try {
    $body = @{ name = $Repo; private = $false; description = $Description } | ConvertTo-Json -Compress
    Invoke-RestMethod -Uri "https://api.github.com/user/repos" -Method Post -Headers @{ Authorization = "Bearer $Token" } -Body $body -ContentType "application/json" | Out-Null
    Write-Host "[OK] Repo creado: https://github.com/$User/$Repo"
} catch {
    Write-Host "[WARN] Repo ya existe o error al crearlo: $($_.Exception.Message) - continuando"
}

$expected = @("serums_banco.html", "serums_banco_data.js", "README.md", "NOTES.md", ".gitignore")
foreach ($f in $expected) {
    if (-not (Test-Path $f)) { Write-Host "[WARN] Falta archivo: $f"; exit 1 }
}

if (-not (Test-Path ".git")) {
    git init -b main | Out-Null
    Write-Host "[OK] git init -b main"
}

$dirty = (git status --porcelain | Out-String).Trim()
if ($dirty) {
    git add -A
    git commit -q -m "Banco SERUMS Medicina Humana 2025-2026 - 400 preguntas (MINSA)"
    Write-Host "[OK] Commit listo"
} else {
    Write-Host "[INFO] Nada que commitear"
}

$originUrl = "https://github.com/$User/$Repo.git"
$remote = (git remote -v) | Select-String -Pattern "origin\s+\S*https"
if ($remote) {
    git remote set-url origin $originUrl
} else {
    git remote add origin $originUrl
}

Write-Host "[INFO] Pusheando a https://github.com/$User/$Repo ..."
git push -u origin main
Write-Host "[OK] Subido: https://github.com/$User/$Repo"
Write-Host "[INFO] Activar GitHub Pages: Settings -> Pages -> Branch: main -> Save"
Write-Host "[INFO] URL del sitio: https://$User.github.io/$Repo/"
