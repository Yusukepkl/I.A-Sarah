param(
    [string]$Destination = "$PSScriptRoot\dados",
    # URL do repositório com os dados mais recentes do Gestor de Alunos
    [string]$RepoUrl = "https://github.com/Yusukepkl/I.A-Sarah.git"
)

if (Test-Path $Destination) {
    git -C $Destination pull
} else {
    git clone $RepoUrl $Destination
}
