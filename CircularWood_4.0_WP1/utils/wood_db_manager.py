"""
Some scripts to help overwriting data in the database for correction etc.
For further questions you can contact me: j.jooshesh@hva.nl
"""

import datetime
import json
import os
from typing import List, Dict

import pandas as pd
from load_dotenv import load_dotenv
import requests

BACKUP_FILEPATH = "./../data_backup/backup_11_09_2023.json"
# CSV_FILEPATH = "./../data_backup/manual_data_entry/340_piecesdatabase.csv"
CSV_FILEPATH = "./../data_backup/data.csv"
SAVING_FILEPATH = ""

load_dotenv()
URL = os.getenv("URL")


class WoodDbManager:
    """
    The class specifically designed for managing a database of residual wood incorporating features for reading
    from a CSV file, cleaning the database, restoring data from a backup, and
    applying corrections to the database entries.
    """

    def __init__(self, fp: str = CSV_FILEPATH, delimiter: str = ";", backup_fp: str = BACKUP_FILEPATH,
                 save_file: str = SAVING_FILEPATH, **kwargs):

        self.fp = fp
        self.backup_fp = backup_fp
        self.save_file = save_file
        self.delimiter = delimiter
        self.access_token = ""

        self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M-%S")
        self.output = []

    @property
    def data_frame(self):
        if self.fp != "":
            return pd.read_csv(self.fp, delimiter=self.delimiter)
        else:
            print('The path to CSV does not exist')
            return None

    def clean_up_data(self, start_index, end_index):
        for index in range(start_index, end_index + 1):
            # print("Deleting row :", index, " -- Request is not sent, this is printed statement only")
            # For safety this request is commented.
            url = URL + "wood/" + (str(index))
            access_token = self.access_token
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + access_token
            }
            r = requests.delete(url=url, headers=headers)
            print(r.json())

    def restore_backup(self):
        all_rows = list()

        with open(self.backup_fp, 'r') as back_up_data:
            rows = json.load(back_up_data)

            for i in range(0, len(rows)):
                del rows[i]['id']

                for j in range(len(rows)):
                    for key in rows[i]:
                        if rows[i][key] is None:
                            if key != 'price':
                                rows[i][key] = ""
                            else:
                                rows[i][key] = 0

                all_rows.append(rows[i])

            for row in all_rows:
                body = json.dumps(row)

                # For safety this is disabled

                resp = requests.post(
                    url=f"{URL}wood",
                    headers={'Content-Type': 'application/json'},
                    data=body
                )
                print(resp.json())

    @staticmethod
    def register():
        inputs = {
            "username": "javid",
            "password": "12345"
        }

        payload = json.dumps(inputs)
        r = requests.post(url=URL + "register", data=payload, headers={"Content-Type": "application/json"})
        print(r.json())

    def login(self):
        credentials = {
            "username": "javid",
            "password": "12345"
        }
        payload = json.dumps(credentials)

        r = requests.post(url=URL + "login", data=payload, headers={"Content-Type": "application/json"})
        self.access_token = r.json()['access_token']
        print(r.json())

    def logout(self):
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.access_token
        }

        r = requests.post(url=URL + "logout", headers=headers)
        print(r.json())

    def filter_removed_ids_from_csv(self):

        self.compile_data_from_csv()

        ids_from_csv = []
        all_ids = []

        for row in self.output:
            ids_from_csv.append(row['id'])
        resp = requests.get(url=f"{URL}wood")
        for r in resp.json():
            all_ids.append(r['id'])

        ids_to_delete = set(all_ids).difference(ids_from_csv)

        access_token = self.access_token

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + access_token
        }

        for i in sorted(ids_to_delete):
            resp = requests.delete(
                url=f"{URL}wood/{i}",
                headers=headers
            )
            print(resp.json())

    def update_specified_rows(self, row_id: int, data: List[Dict]):
        payload = []

        for row in data:
            if row_id == row['id']:
                updating_row = row.copy()
                del updating_row['id']
                del updating_row['timestamp']
                payload.append(updating_row)
        print(payload[0])
        json_payload = json.dumps(payload[0])
        access_token = self.access_token
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + access_token
        }

        resp = requests.patch(
            url=f"{URL}wood/{row_id}",
            headers=headers,
            data=json_payload
        )
        print(resp.json())

    @staticmethod
    def save_row_to_csv(start_row: int, end_row: int):
        rows = []
        try:
            for i in range(start_row, end_row + 1):
                response = requests.get(
                    url=URL + f"wood/{str(i)}",
                    headers={"Content-Type": "application/json"}
                )
                print("Request {0}".format(i))
                if response.status_code == 404:
                    continue
                else:
                    rows.append(response.json())
            for r in rows:
                print(r)
            try:
                json_data = json.dumps(rows)
                df = pd.read_json(json_data)
                df.to_csv("./../data_backup/test_.csv", index=False, sep=";")
            except TypeError:
                pass
        except KeyboardInterrupt:
            pass

    def compile_data_from_csv(self):

        df = self.data_frame
        df = df.fillna('')

        # Verify with the latest schema first
        try:
            for index, row in df.iterrows():
                d = {
                    "id": int(row['id']),
                    "length": float(row['length']),
                    "name": "Red oak FSC",
                    "width": float(row['width']),
                    "height": float(row['height']),
                    "weight": float(row['weight']),
                    "color": row["color"],
                    "reserved": False,
                    "reservation_name": "",
                    "reservation_time": "",
                    "type": "hardwood",
                    "price": 0.0,
                    "source": "HvA Jakoba Mulderhuis (JMH)",
                    "timestamp": self.timestamp,
                    "info": row['info'],
                    "density": int(float(row['weight']) / (
                            float(row['length']) * float(row['width']) * float(row['height'])) * 1000000),
                    "storage_location": row['storage_location'],
                    "intake_id": 1,
                    "wood_species": row["wood_species"]
                }
                self.output.append(d)
        except ValueError:
            pass
        return self.output


if __name__ == "__main__":
    """
    WARNING: 

    *** ONLY RUN THE FOLLOWING FUNCTIONS IF YOU KNOW WHAT YOU ARE DOING! THIS CAN
    LEAD TO MESSING UP WITH THE DATA IN THE WOOD DATABASE ***

    ===============================================================================
        SET OF FUNCTIONS TO EITHER DELETE ALL DATA OR RESTORE ACCORDING TO THE BACKUP.
        FOR NOW THEY ARE COMMENTED OUT TO PREVENT ACCIDENTAL EXECUTION.
    ===============================================================================
    """

    # INITIALIZING THE CLASS
    out = WoodDbManager()

    # REGISTER
    # out.register()

    # LOGIN
    out.login()

    # REMOVE THE NON-EXISTING ID
    # out.filter_removed_ids_from_csv()

    # INSERT DATA FROM CSV TO DB
    out.compile_data_from_csv()

    # UPDATE ROWS BY ID
    # for r in out.output:
    #     out.update_specified_rows(r['id'], out.output)

    # UPDATE ALL THE ROWS FOR CORRECTION OF DATA
    # out.apply_correction()

    # READ AND RESTORE A BACKUP FILE
    # out.restore_backup()

    # REMOVE ROWS FROM DB BASED ON RANGE OF ID
    # out.clean_up_data(1, 459)

    # SAVE ROWS INTO CSV
    # out.save_row_to_csv(1, 568)

    # LOG OUT
    # out.logout()
