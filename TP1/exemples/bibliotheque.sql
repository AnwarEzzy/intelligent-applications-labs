-- Exemple pour la démonstration : ce fichier est lu comme texte, jamais exécuté.
CREATE TABLE auteurs (
    id INTEGER PRIMARY KEY,
    nom TEXT NOT NULL,
    pays TEXT
);

CREATE TABLE livres (
    id INTEGER PRIMARY KEY,
    titre TEXT NOT NULL,
    auteur_id INTEGER NOT NULL,
    annee INTEGER,
    FOREIGN KEY (auteur_id) REFERENCES auteurs(id)
);

INSERT INTO auteurs (id, nom, pays) VALUES (1, 'Tahar Ben Jelloun', 'Maroc');
INSERT INTO livres (id, titre, auteur_id, annee)
VALUES (1, 'La Nuit sacrée', 1, 1987);
