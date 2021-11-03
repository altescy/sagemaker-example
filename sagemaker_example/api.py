from pathlib import Path

import fastapi

from sagemaker_example import iris


def create_app(dataset_path: Path, artifact_path: Path) -> fastapi.FastAPI:
    app = fastapi.FastAPI()
    app.state.model = iris.load_model(artifact_path)

    def ping() -> str:
        return "pong"

    def invocations(data, request: fastapi.Request):  # type: ignore
        model = request.app.state.model
        return iris.predict(model, data)

    invocations.__annotations__["data"] = iris.predict.__annotations__["data"]
    invocations.__annotations__["return"] = iris.predict.__annotations__["return"]

    app.get("/ping")(ping)
    app.post("/invocations")(invocations)

    return app
