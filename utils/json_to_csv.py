import pandas as pd
import json


def json_to_csv(json_file: str, csv_destination: str):
        
    with open(json_file, "r") as file:
        data = json.load(file)
        json_data = json.dumps(data)

    df = pd.read_json(json_data)
    df.to_csv(csv_destination, index=False, sep=";")
