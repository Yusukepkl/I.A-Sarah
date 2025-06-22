param(
    [string]$Destination = "$PSScriptRoot\dados",
    # Repositório de onde baixar os dados (pode ser alterado)
    [string]$RepoUrl = "https://github.com/Yusukepkl/I.A-Sarah.git"
)

if (Test-Path $Destination) {
    git -C $Destination pull
} else {
    git clone $RepoUrl $Destination
}
