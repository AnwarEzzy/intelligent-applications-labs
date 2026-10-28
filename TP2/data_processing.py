"""Chargement et préparation du jeu de données Auto MPG."""

from pathlib import Path

import pandas as pd


DATA_PATH = Path(__file__).resolve().parent / "data" / "mpg.csv"
MPG_TO_L_PER_100KM = 235.214583
POUNDS_TO_KG = 0.45359237


def load_vehicles(path: Path = DATA_PATH) -> pd.DataFrame:
    """Charge la copie locale du CSV Seaborn et ajoute des unités lisibles."""
    vehicles = pd.read_csv(path)
    expected = {
        "mpg", "cylinders", "displacement", "horsepower", "weight",
        "acceleration", "model_year", "origin", "name",
    }
    missing = expected.difference(vehicles.columns)
    if missing:
        raise ValueError(f"Colonnes absentes du CSV : {', '.join(sorted(missing))}")

    return vehicles.assign(
        year=vehicles["model_year"] + 1900,
        weight_kg=vehicles["weight"] * POUNDS_TO_KG,
        consumption_l_100km=MPG_TO_L_PER_100KM / vehicles["mpg"],
    )


def filter_vehicles(
    vehicles: pd.DataFrame,
    origins: list[str],
    years: tuple[int, int],
    cylinders: list[int],
    minimum_mpg: float = 0.0,
) -> pd.DataFrame:
    """Applique les filtres de l'analyse descriptive seulement."""
    return vehicles.loc[
        vehicles["origin"].isin(origins)
        & vehicles["year"].between(*years)
        & vehicles["cylinders"].isin(cylinders)
        & vehicles["mpg"].ge(minimum_mpg)
    ].copy()


def display_table(vehicles: pd.DataFrame) -> pd.DataFrame:
    """Prépare les colonnes et unités du tableau de démonstration."""
    columns = {
        "name": "Véhicule",
        "origin": "Origine",
        "year": "Année",
        "cylinders": "Cylindres",
        "mpg": "Efficacité (mpg)",
        "consumption_l_100km": "Consommation (L/100 km)",
        "horsepower": "Puissance (hp)",
        "weight_kg": "Poids (kg)",
        "acceleration": "Accélération (s)",
    }
    return vehicles[list(columns)].rename(columns=columns).round(2)
