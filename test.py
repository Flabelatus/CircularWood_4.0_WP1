from api.api_callback import api_call
import json


def add_wood():
    base_file = 'wood.json'

    with open(base_file) as wood_json:
        data = json.load(wood_json)

    response = api_call("/waste_wood", payload=data, method="POST")
    print(response)


if __name__ == "__main__":
    add_wood()
