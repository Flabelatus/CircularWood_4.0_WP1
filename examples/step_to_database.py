import requests

with open("stp/stool_leg_test.stp", "r") as rapid_file:
    instructions = rapid_file.read()
    escaped = instructions.replace('"', '\\"')

design = {
    "part_file_path": escaped,
    "part": "leg_01",
    "wood_id": 1,
    "part_name": 1,
    "project_id": "ABC-123",
    "tag": "stool"
}

# resp = requests.post(
#     url="https://robotlab-residualwood.onrender.com/design/client",
#     headers={"Content-Type": "application/json"},
#     json=design
# )

# print(resp.json())
