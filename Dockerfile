FROM python:3.8-slim

WORKDIR /app

RUN pip install -U poetry
COPY pyproject.toml ./pyproject.toml
COPY poetry.lock ./poetry.lock
RUN poetry install --no-dev

COPY sagemaker_example/ ./sagemaker_example/

EXPOSE 8080
ENTRYPOINT ["poetry", "run", "python", "-m", "sagemaker_example"]
