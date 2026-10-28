# À lancer dans le terminal PowerShell de l'utilisateur depuis TP2.
# Crée trois commits TP2, puis pousse un commit à la fois sans forcer l'historique.
$ErrorActionPreference = 'Stop'
$repo = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path

function Invoke-Git {
    param([string[]]$Arguments)
    & git -C $repo @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Échec de git $($Arguments -join ' ') (code $LASTEXITCODE)."
    }
}

$branch = (& git -C $repo branch --show-current).Trim()
if ($LASTEXITCODE -ne 0 -or $branch -ne 'main') {
    throw "Ouvre la branche main du dépôt avant de publier TP2. Branche actuelle : $branch"
}

$origin = (& git -C $repo remote get-url origin).Trim()
if ($LASTEXITCODE -ne 0 -or $origin -notmatch '^https://github\.com/AnwarEzzy/intelligent-applications-labs(?:\.git)?$') {
    throw "Le dépôt origin n'est pas le dépôt GitHub attendu : $origin"
}

$staged = @(& git -C $repo diff --cached --name-only)
if ($LASTEXITCODE -ne 0 -or $staged.Count -gt 0) {
    throw 'Des fichiers sont déjà préparés (staged). Vérifie-les avant de lancer ce script.'
}

# Le README principal doit permettre de retrouver TP2 depuis la page du dépôt.
$rootReadme = Join-Path $repo 'README.md'
$readmeText = [System.IO.File]::ReadAllText($rootReadme)
$tp2Row = '| [TP2](TP2/README.md) | Analyse Auto MPG et prédiction de consommation | Streamlit, Plotly, scikit-learn |'
if (-not $readmeText.Contains('| [TP2](TP2/README.md)')) {
    $tp1Position = $readmeText.IndexOf('| [TP1](TP1/README.md)')
    if ($tp1Position -lt 0) { throw 'Ligne TP1 introuvable dans le README principal.' }
    $lineEnd = $readmeText.IndexOf("`n", $tp1Position)
    if ($lineEnd -lt 0) { throw 'Fin de ligne TP1 introuvable dans le README principal.' }
    $newline = if ($readmeText.Contains("`r`n")) { "`r`n" } else { "`n" }
    $readmeText = $readmeText.Insert($lineEnd + 1, $tp2Row + $newline)
    [System.IO.File]::WriteAllText($rootReadme, $readmeText, [System.Text.UTF8Encoding]::new($false))
}

$groups = @(
    @{
        Message = 'Add Auto MPG data and Random Forest model'
        Paths = @('TP2/data/mpg.csv', 'TP2/data_processing.py', 'TP2/model.py')
    },
    @{
        Message = 'Build AutoScope Streamlit dashboard'
        Paths = @('TP2/app.py', 'TP2/requirements.txt', 'TP2/.streamlit/config.toml')
    },
    @{
        Message = 'Document and verify TP2'
        Paths = @('README.md', 'TP2/README.md', 'TP2/tests/test_tp2.py', 'TP2/.gitignore', 'TP2/publish_tp2.ps1')
    }
)

foreach ($group in $groups) {
    Invoke-Git -Arguments (@('add', '--') + $group.Paths)
    & git -C $repo diff --cached --quiet
    if ($LASTEXITCODE -eq 1) {
        Invoke-Git -Arguments @('commit', '-m', $group.Message)
    } elseif ($LASTEXITCODE -ne 0) {
        throw 'Impossible de vérifier les fichiers préparés.'
    }
}

# GitHub peut déjà contenir les commits TP1. Pousser uniquement les commits manquants,
# du plus ancien au plus récent, permet de voir chaque modification séparément.
$remoteLine = @(& git -C $repo ls-remote origin refs/heads/main)
if ($LASTEXITCODE -ne 0) {
    throw 'Impossible de joindre GitHub. Les commits locaux sont conservés ; relance ce script quand la connexion fonctionne.'
}
$remoteHash = if ($remoteLine.Count -gt 0) { ($remoteLine[0] -split '\s+')[0] } else { $null }
$history = @(& git -C $repo rev-list --reverse main)
if ($LASTEXITCODE -ne 0) { throw 'Impossible de lire l’historique local.' }

$remoteIndex = -1
if ($remoteHash) {
    $remoteIndex = [array]::IndexOf($history, $remoteHash)
    if ($remoteIndex -lt 0) {
        throw 'La branche GitHub main a un historique différent. Arrêt sans écraser les commits distants.'
    }
}

for ($index = $remoteIndex + 1; $index -lt $history.Count; $index++) {
    $commit = $history[$index]
    Write-Host "Publication du commit $commit..."
    Invoke-Git -Arguments @('push', 'origin', "${commit}:refs/heads/main")
}

Write-Host 'TP2 publié : chaque commit a été poussé séparément.'
