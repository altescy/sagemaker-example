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

3. Train a model with SageMaker

```
poetry run python scripts/train.py \
    --dataset-path s3://your-bucket/path/to/dataset \
    --artifact-path s3://your-bucket/path/to/artifacts \
    --image-uri xxxxxxxxxxxx.dkr.ecr.ap-northeast-1.amazonaws.com/your-image-name \
    --execution-role arn:aws:iam::xxxxxxxxxxxx:role/SageMakerExecutionRole
```

4. Deploy the trained model

```
poetry run python scripts/deploy.py \
    --endpoint-name your-endpoint-name \
    --training-job training-job-name
```

5. Invoke the endpoint

```
poetry run python scripts/predict.py -n your-endpoint-name data/test.json
```

6. Delete the endpoint

```
aws sagemaker delete-endpoint --endpoint-name your-endpoint-name
```

## Local mode

1. Train a model on your local machie

```
poetry run python -m sagemaker_example train --local
```

2. Serve the endpoint on your local machine

```
poetry run python -m sagemaker_example serve --local --port 8080
```

3. Train a model with local mode

```
poetry run python scripts/train.py \
    --local \
    --dataset-path file://`pwd`/data \
    --artifact-path file://`pwd`/data \
    --image-uri xxxxxxxxxxxx.dkr.ecr.ap-northeast-1.amazonaws.com/your-image-name \
    --execution-role dummy/dummy
```
