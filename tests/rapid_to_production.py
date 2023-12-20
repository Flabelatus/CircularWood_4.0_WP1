import json
import requests

with open("rapid/milling_sample.mod", "r") as rapid_file:
    instructions = rapid_file.read()
    escaped = instructions.replace('"', '\\"')

prod = {
    "status": "pending",
    "instruction": escaped,
    "operation": "milling",
    "wood_id": 1,
    "instruction_type": "rapid"
}


resp = requests.get(
    url="https://robotlab-residualwood.onrender.com/production/6",
    headers={"Content-Type": "application/json"},
    # json=prod
)

print(json.loads(resp.content)["instruction"])
