# TP1 — Assistant pédagogique Flask

Pour transmettre ce projet à un camarade, utiliser `TP1-partage.zip` et le
guide [README_PARTAGE.md](README_PARTAGE.md).

Application de démonstration pour la séance : discussions multiples, spécialité,
historique SQLite, import de fichier, résumé/questions sur le fichier, export
JSON, remise à zéro et évaluation colorée des réponses.

## Démarrer dans VS Code (Windows)

1. Ouvrir **ce dossier `TP1`** dans VS Code.
2. Dans `Ctrl+Shift+P` → **Python: Select Interpreter**, choisir
   `.venv\Scripts\python.exe` (Python 3.11).
3. Installer les dépendances Python dans un environnement local :

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

4. Lancer l'application :

```powershell
.\.venv\Scripts\python.exe app.py
```

Ouvrir <http://127.0.0.1:5000/>. Le CSS compilé est inclus dans le dépôt.
Si vous modifiez les styles et avez Node.js, lancer `npm.cmd install`, puis
`npm.cmd run css:watch` dans un deuxième terminal.

## Démonstration rapide pour le professeur

1. Choisir **Bases de données / SQL** dans la liste des spécialités.
2. Importer [`exemples/bibliotheque.sql`](exemples/bibliotheque.sql). Le SQL est
   seulement lu comme document, jamais exécuté dans la base de l'application.
3. Demander : **Quelles tables contient ce fichier ?**, puis
   **Résume ce fichier**.
4. Cliquer sur **👍 Utile** : la réponse devient verte. Cliquer sur
   **👎 À améliorer** : elle devient rouge. La note est enregistrée dans SQLite.
5. Créer une nouvelle discussion, puis revenir à l'ancienne avec la liste
   déroulante. Les messages sont conservés après redémarrage du serveur.
6. Exporter une discussion, puis toutes les discussions au format JSON.
7. Cliquer sur **Vider la conversation** pour effacer les messages et le
   document de la discussion sélectionnée.

## Mode IA et mode démo local

Sans clé API, l'interface affiche **Mode démo local**. Elle peut extraire des
passages d'un fichier, produire un court résumé extractif et reconnaître les
tables d'un fichier SQL. Elle ne prétend pas fournir une réponse IA générale.

Si vous avez une clé API, copier `.env.example` vers `.env`, puis renseigner
`OPENAI_API_KEY` dans **votre fichier local**. Ne partagez pas cette clé. Le
projet utilise la version `openai==0.27.10` demandée dans le support de cours ; la clé est
utilisée côté serveur seulement. Le modèle est réglable avec `OPENAI_MODEL`.

Fichiers acceptés : TXT, MD, CSV, JSON et SQL (2 Mo au maximum ; texte limité
à 100 000 caractères). L'import de PDF n'est pas inclus dans cette version.

## Vérifier

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

La base est créée automatiquement dans `instance/chat.sqlite3` au premier
lancement. Le dossier `instance` et `.env` sont ignorés par Git.
