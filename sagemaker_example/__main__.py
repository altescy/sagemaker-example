import argparse
import os
from pathlib import Path

import uvicorn

from sagemaker_example import api, iris

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
    parser = argparse.ArgumentParser()
    parser.add_argument("command", type=str)
    parser.add_argument("--local", action="store_true")
    parser.add_argument("--host", type=str, default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args()

    if args.local:
        dataset_path = Path("data/")
        artifact_path = Path("data/")
    else:
        dataset_path = Path("/opt/ml/input/data/training/")
        artifact_path = Path("/opt/ml/model/")

    if args.command == "train":
        iris.train(dataset_path, artifact_path)
    elif args.command == "serve":
        app = api.create_app(dataset_path, artifact_path)
        uvicorn.run(app, host=args.host, port=args.port)
    else:
        raise ValueError(f"invalid command: {args.command}")


if __name__ == "__main__":
    main()
