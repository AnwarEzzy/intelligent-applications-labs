# TP2 — Analyse et prédiction de la consommation automobile

Application Streamlit réalisée à partir du jeu de données **Auto MPG**. Son interface
**AutoScope** présente trois vues : un tableau de bord, un catalogue de véhicules
et un simulateur de consommation. Les fonctionnalités demandées sont conservées,
avec une présentation différente des captures de référence.

## Lancer dans VS Code sous Windows

Ouvrir le dossier `TP2` dans VS Code. Installer Python 3.11 ou une version plus
récente, puis exécuter dans le terminal PowerShell :

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

L'application s'ouvre normalement à <http://localhost:8501>. Pour l'arrêter,
appuyer sur `Ctrl+C`. Si la commande `python` ne fonctionne pas, essayer `py -3.11`
pour créer l'environnement, puis conserver les deux autres commandes.

Le fichier `data/mpg.csv` est inclus : une connexion Internet n'est pas nécessaire
pour lancer la démonstration. Aucun service externe ni clé API ne sont requis.

## Démonstration pour la séance

1. Dans **Vue d'ensemble**, sélectionner une origine, une période ou des cylindres
   dans la barre latérale. Les indicateurs et les graphiques se mettent à jour.
2. Comparer les consommations par origine, la répartition des voitures et la
   relation entre poids et consommation.
3. Dans **Catalogue des véhicules**, consulter le tableau et choisir un véhicule
   pour afficher sa fiche.
4. Dans **Estimation ML**, renseigner les caractéristiques d'un véhicule et cliquer
   sur **Calculer l'estimation**. Le résultat apparaît en L/100 km et en mpg.

## Méthode

- `mpg` mesure l'efficacité : plus il est élevé, moins le véhicule consomme.
- La conversion est `L/100 km = 235,214583 / mpg`. Le poids passe de livres à
  kilogrammes avec `1 lb = 0,45359237 kg`.
- La consommation moyenne affichée est la moyenne des consommations calculées
  pour chaque véhicule, et non la conversion de la moyenne des mpg.
- Le modèle apprend à prédire les **L/100 km** avec cylindres, cylindrée,
  puissance, poids, accélération, année et origine. Le nom du véhicule est exclu.
- Les données sont séparées en 80 % entraînement / 20 % test avec une graine fixe.
  L'imputation des six puissances manquantes est apprise uniquement sur le jeu
  d'entraînement. L'origine est encodée en variables indicatrices.
- Le score MAE est l'erreur absolue moyenne sur les données de test ; R² donne
  une autre mesure de qualité. Les filtres n'affectent pas l'entraînement.

Les données concernent les années 1970 à 1982 : le modèle est une démonstration
pédagogique et ne prédit pas de manière fiable des véhicules modernes.

## Vérification

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

## Publier dans le dépôt du cours

Dans le terminal PowerShell de VS Code, depuis le dossier `TP2` :

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\publish_tp2.ps1
```

Le script ajoute TP2 au README principal, crée trois commits logiques (données et
modèle, interface, documentation et tests), puis pousse chaque commit séparément.
Il vérifie l'historique distant et n'utilise pas de `force push`. Si GitHub n'est
pas accessible, les commits locaux sont conservés et le script peut être relancé.

## Source et attribution

Quinlan, R. (1993). *Auto MPG* [jeu de données]. UCI Machine Learning Repository.
DOI : <https://doi.org/10.24432/C5859H>. Licence du jeu de données : CC BY 4.0.

Le CSV inclus est une copie du fichier public
<https://raw.githubusercontent.com/mwaskom/seaborn-data/master/mpg.csv>.
Les colonnes calculées (`year`, `weight_kg`, `consumption_l_100km`) sont créées
au chargement ; le CSV d'origine n'est pas modifié.
