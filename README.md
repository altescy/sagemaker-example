# sagemaker-example

This repository provides a simple example of training and deploying your own machine learning model with AWS SageMaker.

## Usage

1. Upload dataset files to S3

```
aws s3 cp ./data/iris.csv s3://your-bucket/path/to/dataset/iris.csv
```

2. Build and push the docker image to ECR

```
./scripts/build_and_push_ecr.sh your-image-name
```

3. Train a model and deploy the inference endpoint

```
poetry run python scripts/deploy.py \
    --endopint-name your-endpoint-name \
    --dataset-path s3://your-bucket/path/to/dataset \
    --artifact-path s3://your-bucket/path/to/artifacts \
    --image-uri xxxxxxxxxxxx.dkr.ecr.ap-northeast-1.amazonaws.com/your-image-name \
    --execution-role arn:aws:iam::xxxxxxxxxxxx:role/SageMakerExecutionRole
```

4. Invoke the endpoint

```
aws sagemaker-runtime invoke-endpoint \
    --endopint-name your-endopint-name \
    --body file://`pwd`/data/test.json \
    --content-type application/json \
    output.json
```

5. Delete the endpoint

```
aws sagemaker delete-endpoint --endpoint-name your-endpoint-name
```

## Local mode

1. Train model on your local machie

```
poetry run python -m sagemaker_example train --local
```

2. Serve the endpoint on your local machine

```
poetry run python -m sagemaker_example serve --local --port 8080
```

3. Invoke the SageMaker endpoint on your local machine

```
poetry run python scripts/deploy.py \
    --endopint-name your-endpoint-name \
    --image-uri xxxxxxxxxxxx.dkr.ecr.ap-northeast-1.amazonaws.com/your-image-name \
    --execution-role arn:aws:iam::xxxxxxxxxxxx:role/SageMakerExecutionRole
```
