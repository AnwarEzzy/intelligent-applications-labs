"""Entraînement du Random Forest pour estimer la consommation."""

from dataclasses import dataclass

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from data_processing import MPG_TO_L_PER_100KM, POUNDS_TO_KG


NUMERIC_FEATURES = [
    "cylinders", "displacement", "horsepower", "weight", "acceleration", "model_year",
]
FEATURES = NUMERIC_FEATURES + ["origin"]


@dataclass(frozen=True)
class ModelResult:
    pipeline: Pipeline
    mae: float
    r2: float
    train_size: int
    test_size: int


def train_model(vehicles: pd.DataFrame) -> ModelResult:
    """Sépare d'abord train/test, puis apprend l'imputation dans le pipeline."""
    x = vehicles[FEATURES]
    y = vehicles["consumption_l_100km"]
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=42
    )

    preprocessing = ColumnTransformer(
        transformers=[
            ("numeric", SimpleImputer(strategy="median"), NUMERIC_FEATURES),
            ("origin", OneHotEncoder(handle_unknown="ignore"), ["origin"]),
        ]
    )
    pipeline = Pipeline(
        steps=[
            ("preprocess", preprocessing),
            ("forest", RandomForestRegressor(
                n_estimators=250, min_samples_leaf=2, random_state=42, n_jobs=-1
            )),
        ]
    )
    pipeline.fit(x_train, y_train)
    predictions = pipeline.predict(x_test)
    return ModelResult(
        pipeline=pipeline,
        mae=float(mean_absolute_error(y_test, predictions)),
        r2=float(r2_score(y_test, predictions)),
        train_size=len(x_train),
        test_size=len(x_test),
    )


def predict_consumption(
    result: ModelResult,
    *,
    cylinders: int,
    displacement: float,
    horsepower: float,
    weight_kg: float,
    acceleration: float,
    year: int,
    origin: str,
) -> tuple[float, float]:
    """Renvoie la consommation prédite et l'efficacité équivalente en mpg."""
    example = pd.DataFrame([{
        "cylinders": cylinders,
        "displacement": displacement,
        "horsepower": horsepower,
        "weight": weight_kg / POUNDS_TO_KG,
        "acceleration": acceleration,
        "model_year": year - 1900,
        "origin": origin,
    }])
    consumption = float(result.pipeline.predict(example)[0])
    return consumption, MPG_TO_L_PER_100KM / consumption
