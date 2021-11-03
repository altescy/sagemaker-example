import argparse
import os

from sagemaker.estimator import Estimator


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--endpoint-name", type=str, required=True)
    parser.add_argument("-i", "--image-uri", type=str, required=True)
    parser.add_argument("-r", "--execution-role", type=str, required=True)
    parser.add_argument("--dataset-path", type=str, default=None)
    parser.add_argument("--artifact-path", type=str, default=None)
    parser.add_argument("--training-instance", type=str, default="ml.m5.large")
    parser.add_argument("--inference-instance", type=str, default="ml.t2.medium")
    parser.add_argument("--local", action="store_true")
    args = parser.parse_args()

    role = args.execution_role
    image_uri = args.image_uri
    endpoint_name = args.endpoint_name

    if args.local:
        training = f"file://{os.path.abspath('./data')}"
        output = f"file://{os.path.abspath('./data')}"
        training_instance_type = "local"
        inference_instance_type = "local"
    else:
        training = args.dataset_path
        output = args.artifact_path
        training_instance_type = args.training_instance
        inference_instance_type = args.inference_instance

    estimator = Estimator(
        image_uri=image_uri,
        role=role,
        instance_count=1,
        instance_type=training_instance_type,
        output_path=output,
    )

    estimator.fit({"training": training})

    estimator.deploy(
        endpoint_name=endpoint_name,
        instance_type=inference_instance_type,
        initial_instance_count=1,
    )


if __name__ == "__main__":
    main()
