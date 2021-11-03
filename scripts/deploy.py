import argparse

from sagemaker.estimator import Estimator


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--endpoint-name", type=str, required=True)
    parser.add_argument("-t", "--training-job", type=str, required=True)
    parser.add_argument("--instance-type", type=str, default="ml.m5.large")
    parser.add_argument("--instance-count", type=int, default=1)
    args = parser.parse_args()

    endpoint_name = args.endpoint_name
    training_job_name = args.training_job

    instance_type = args.instance_type
    instance_count = args.instance_count

    estimator = Estimator.attach(training_job_name)

    estimator.deploy(
        endpoint_name=endpoint_name,
        instance_type=instance_type,
        initial_instance_count=instance_count,
    )


if __name__ == "__main__":
    main()
