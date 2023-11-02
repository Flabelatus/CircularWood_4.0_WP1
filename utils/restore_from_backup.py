import json

with open("./../data_backup/backup.json", 'r') as r:
    d = json.load(r)
    print(len(d))