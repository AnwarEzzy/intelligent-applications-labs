# Lancer TP1 sur un autre PC Windows

Cette archive contient le code source et le CSS déjà généré. **Poetry et
Node.js ne sont pas nécessaires** pour montrer l'application. Il faut Python
3.11 et une connexion Internet pour installer les bibliothèques Python.

## 1. Installer Python 3.11 si nécessaire

Ouvrir PowerShell et vérifier :

```powershell
py -3.11 --version
```

Si Python 3.11 n'est pas disponible, l'installer avec WinGet :

```powershell
winget install --id Python.Python.3.11 --exact --source winget
```

Fermer puis rouvrir PowerShell après l'installation. Si WinGet n'existe pas,
télécharger **Windows installer (64-bit)** depuis
<https://www.python.org/downloads/release/python-3119/>, l'installer, puis
rouvrir PowerShell.

## 2. Extraire l'archive et créer l'environnement

Si `TP1-partage.zip` est dans `Téléchargements` :

```powershell
cd "$env:USERPROFILE\Downloads"
Expand-Archive -LiteralPath ".\TP1-partage.zip" -DestinationPath ".\TP1-demo"
cd ".\TP1-demo\TP1"
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Si `py -3.11` n'est pas reconnu mais `python --version` affiche bien Python
3.11, remplacer la ligne de création par `python -m venv .venv`.

## 3. Lancer

```powershell
.\.venv\Scripts\python.exe app.py
```

Ouvrir <http://127.0.0.1:5000/>. Laisser le terminal ouvert ; `Ctrl+C` arrête
le serveur.

Pour la démo : choisir **Bases de données / SQL**, importer
`exemples\bibliotheque.sql`, demander **Quelles tables contient ce fichier ?**
puis **Résume ce fichier**. Le mode sans clé API fonctionne localement.

La base SQLite `instance\chat.sqlite3` est créée automatiquement au premier
lancement. L'archive ne contient ni conversations personnelles ni clé API.
