param(
    [string]$Destination = "$PSScriptRoot\dados",
    [string]$RepoUrl = "https://github.com/usuario/I.A-Sarah.git"
)

if (Test-Path $Destination) {
    git -C $Destination pull
} else {
    git clone $RepoUrl $Destination
}
