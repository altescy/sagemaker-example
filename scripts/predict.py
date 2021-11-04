import argparse
import json
import os

import boto3
import sagemaker
from sagemaker.predictor import Predictor

aws_profile = os.environ.get("AWS_PROFILE")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=str)
    parser.add_argument("-n", "--endpoint-name", type=str, required=True)
    args = parser.parse_args()

    boto_session = boto3.Session(profile_name=aws_profile)
    session = sagemaker.Session(boto_session=boto_session)

    predictor = Predictor(
        endpoint_name=args.endpoint_name,
        sagemaker_session=session,
        serializer=sagemaker.serializers.JSONSerializer(),
        deserializer=sagemaker.deserializers.JSONDeserializer(),
    )

    with open(args.input) as jsonfile:
        data = json.load(jsonfile)

    response = predictor.predict(data)
    print(response)


if __name__ == "__main__":
    main()
