# Compila o instalador do Gestor de Alunos usando o Inno Setup

param(
    [string]$InnoPath = "$Env:ProgramFiles\Inno Setup 6\ISCC.exe"
)

# Caminho do repositório (este script está na pasta "installer")
$repo = (Resolve-Path "$PSScriptRoot\..\").Path

# Gera o executável com o PyInstaller
& "$repo\scripts\build_exe.ps1"

# Caminho do executável do Inno Setup (pode ser ajustado pelo parâmetro)
if (-not (Test-Path $InnoPath)) {
    Write-Error "ISCC.exe não encontrado em $InnoPath"
    exit 1
}

# Compila o instalador apontando para a raiz do repositório
& $InnoPath "$repo\installer\installer.iss" /DSourceRoot="$repo"
