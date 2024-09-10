import json
import os
from os import path


current_dir = os.getcwd()
fp = path.join(current_dir, "idemat", "idenmat_2023_wood_simplified.json")
name = "Spruce, European FSC/PEFC"
with open(fp) as idemat_json:
    content = json.load(idemat_json)

    for mat in content:
        if name in mat["process"]:
            print(mat)


