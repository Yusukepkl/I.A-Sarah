# Compila o instalador do Gestor de Alunos usando o Inno Setup

# Caminho do repositório
$repo = "C:\Users\jhona\Documents\GitHub\I.A-Sarah"

# Caminho do executável do Inno Setup (ajuste se estiver instalado em outro lugar)
$inno = "C:\Program Files (x86)\Inno Setup 6\ISCC.exe"

& $inno "$repo\installer\installer.iss" /DSourceRoot="$repo"
