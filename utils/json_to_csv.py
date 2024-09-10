import pandas as pd
import json


with open("./../data_backup/backup_11_09_2023.json", "r") as file:
    data = json.load(file)
    json_data = json.dumps(data)

df = pd.read_json(json_data)
df.to_csv("./../data_backup/test_.csv", index=False, sep=";")

