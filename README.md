# Travaux pratiques — Applications intelligentes

Ce dépôt regroupe les travaux pratiques des deux modules :

- **Développement d'applications intelligentes**
- **Déploiement d'applications intelligentes**

Chaque TP est placé dans un dossier numéroté (`TP1`, `TP2`, etc.) pour suivre
la progression des séances.

| Dossier | Sujet | Technologies |
| --- | --- | --- |
| [TP1](TP1/README.md) | Assistant pédagogique avec discussions, fichiers et évaluations | Flask, SQLite, Tailwind CSS |

## Démarrer TP1 sur Windows

Python 3.11 est requis. Le CSS est déjà généré ; Node.js et Poetry ne sont pas
nécessaires pour lancer l'application.

```powershell
cd TP1
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

Ouvrir <http://127.0.0.1:5000/>. Voir le [guide TP1](TP1/README.md) pour la
démonstration et les détails des fonctionnalités. Sans clé API, l'application
utilise un mode local extractif pour les documents importés.
