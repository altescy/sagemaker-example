import argparse
import os

import boto3
import sagemaker
from sagemaker.estimator import Estimator

aws_profile = os.environ.get("AWS_PROFILE")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--image-uri", type=str, required=True)
    parser.add_argument("-r", "--execution-role", type=str, required=True)
    parser.add_argument("--dataset-path", type=str, required=True)
    parser.add_argument("--artifact-path", type=str, required=True)
    parser.add_argument("--instance-type", type=str, default="ml.m5.large")
    parser.add_argument("--instance-count", type=int, default=1)
    parser.add_argument("--local", action="store_true")
    args = parser.parse_args()

    role = args.execution_role
    image_uri = args.image_uri
    training = args.dataset_path
    output = args.artifact_path

    if args.local:
        instance_type = "local"
        instance_count = 1
    else:
        instance_type = args.instance_type
        instance_count = args.instance_count

    boto_session = boto3.Session(profile_name=aws_profile)
    sagemaker_session = sagemaker.Session(boto_session=boto_session)

    estimator = Estimator(
        image_uri=image_uri,
        role=role,
        instance_count=instance_count,
        instance_type=instance_type,
        output_path=output,
        sagemaker_session=sagemaker_session,
    )

    estimator.fit({"training": training})

    print(estimator.latest_training_job.name)


if __name__ == "__main__":
    main()
