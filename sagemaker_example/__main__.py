import os
import sys
from pathlib import Path

import uvicorn

from sagemaker_example import iris, api

if os.environ.get("LOCAL_MODE"):
    dataset_path = Path("data/")
    artifact_path = Path("data/")
else:
    dataset_path = Path("/opt/ml/input/data/training/")
    artifact_path = Path("/opt/ml/model/")


def train() -> None:
    global dataset_path, artifact_path
    iris.train(dataset_path, artifact_path)


def serve() -> None:
    global dataset_path, artifact_path
    app = api.create_app(dataset_path, artifact_path)
    uvicorn.run(app, host="0.0.0.0", port=8080)


def main() -> None:
    command = sys.argv[1]

    if command == "train":
        train()
    elif command == "serve":
        serve()
    else:
        raise ValueError(f"invalid command: {command}")


if __name__ == "__main__":
    main()
