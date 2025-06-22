# Compila o instalador do Gestor de Alunos usando o Inno Setup

# Caminho do repositório (este script está na pasta "installer")
$repo = (Resolve-Path "$PSScriptRoot\..\").Path

# Caminho do executável do Inno Setup (ajuste se estiver instalado em outro lugar)
$inno = "C:\Program Files (x86)\Inno Setup 6\ISCC.exe"

& $inno "$repo\installer\installer.iss" /DSourceRoot="$repo"
