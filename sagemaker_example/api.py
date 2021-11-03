from pathlib import Path

import fastapi

from sagemaker_example import model


def create_app(dataset_path: Path, artifact_path: Path) -> fastapi.FastAPI:
    app = fastapi.FastAPI()
    app.state.model = model.load(artifact_path)

    def ping() -> str:
        return "pong"

    def invocations(data, request: fastapi.Request):  # type: ignore
        return model.predict(request.app.state.model, data)

    invocations.__annotations__["data"] = model.predict.__annotations__["data"]
    invocations.__annotations__["return"] = model.predict.__annotations__["return"]

    app.get("/ping")(ping)
    app.post("/invocations")(invocations)

    return app
