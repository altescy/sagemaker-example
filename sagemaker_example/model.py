import csv
import pickle
from pathlib import Path
from typing import List

import numpy
from pydantic import BaseModel
from sklearn.ensemble import RandomForestClassifier


class Instance(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float


def train(dataset_path: Path, artifact_path: Path) -> None:
    features: List[List[float]] = []
    targets: List[int] = []
    with open(dataset_path / "iris.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            features.append(
                [
                    float(row["sepal_length"]),
                    float(row["sepal_width"]),
                    float(row["petal_length"]),
                    float(row["petal_width"]),
                ]
            )
            targets.append(int(row["target"]))

    X = numpy.asarray(features)
    y = numpy.asarray(targets)

    model = RandomForestClassifier()
    model.fit(X, y)

    with open(artifact_path / "model.pkl", "wb") as pklfile:
        pickle.dump(model, pklfile)


def load(artifact_path: Path) -> RandomForestClassifier:
    with open(artifact_path / "model.pkl", "rb") as pklfile:
        return pickle.load(pklfile)


def predict(model: RandomForestClassifier, data: List[Instance]) -> List[int]:
    X = numpy.array([[x.sepal_length, x.sepal_width, x.petal_length, x.petal_width] for x in data])
    return model.predict(X).tolist()  # type: ignore
