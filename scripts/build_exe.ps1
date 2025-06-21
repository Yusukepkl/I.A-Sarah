# Gera o executável do Gestor de Alunos usando PyInstaller
param(
    [string]$Entry = "src/main.py",
    [string]$Name = "gestor-alunos"
)

python -m PyInstaller --onefile --name $Name $Entry
