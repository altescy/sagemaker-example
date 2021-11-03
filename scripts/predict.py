import argparse
import json

import sagemaker
from sagemaker.predictor import Predictor


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=str)
    parser.add_argument("-n", "--endpoint-name", type=str, required=True)
    args = parser.parse_args()

    session = sagemaker.Session()
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
