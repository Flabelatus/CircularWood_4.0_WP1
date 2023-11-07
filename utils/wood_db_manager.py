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

BACKUP_FILEPATH = "./../data_backup/backup_11_03_2023.json"
CSV_FILEPATH = "./../data_backup/manual_data_entry/340_piecesdatabase.csv"
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

        self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M-%S")
        self.output = []

    @property
    def data_frame(self):
        if self.fp != "":
            return pd.read_csv(self.fp, delimiter=self.delimiter)
        else:
            print('The path to CSV does not exist')
            return None

    @staticmethod
    def clean_up_data(start_index, end_index):
        for index in range(start_index, end_index + 1):
            # print("Deleting row :", index, " -- Request is not sent, this is printed statement only")
            # For safety this request is commented.
            url = URL + "residual_wood/" + (str(index))
            access_token = ""
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
                    url=f"{URL}residual_wood",
                    headers={'Content-Type': 'application/json'},
                    data=body
                )
                print(resp.json())

    def apply_correction(self):
        updated_rows = []
        with open(self.backup_fp, 'r') as back_up_data:
            existing_rows = json.load(back_up_data)
            for i in range(400, 458):
                # delete this field as it's not needed to update
                del existing_rows[i]['timestamp']
                existing_rows[i]['source'] = "Hooidrift 129B"
                existing_rows[i]['name'] = "Red oak FSC"
                existing_rows[i]['price'] = 0.27

                # Here you can add any changes needed to update the database
                #

                # After the changes, add them to th rows
                updated_rows.append(existing_rows[i])

        # update all the rows
        for r in updated_rows:
            new_row = r.copy()
            del new_row['id']

            payload = json.dumps(new_row)

            print(r['id'], "This is just printed statement, the request is not sent", r['name'])

            # For safety this is disabled

            # r = requests.patch(
            #     url=f"https://robotlab-residualwood.onrender.com/residual_wood/{r['id']}",
            #     headers={'Content-Type': 'application/json'},
            #     data=payload
            # )
            # print(r)

    def filter_removed_ids_from_csv(self):

        self.compile_data_from_csv()

        ids_from_csv = []
        all_ids = []

        for row in self.output:
            ids_from_csv.append(row['id'])
        resp = requests.get(url=f"{URL}residual_wood")
        for r in resp.json():
            all_ids.append(r['id'])

        ids_to_delete = set(all_ids).difference(ids_from_csv)

        jwt_token = ("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNjk5Mzc2NjY4LCJqdGkiOiJlOGZjY"
                     "WVkZC0yZmYzLTRhYzMtOTRlMy1hYmM4Y2JlMTFiM2UiLCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoxLCJuYmYiOjE2OTkzNzY"
                     "2NjgsImV4cCI6MTY5OTM3NzU2OCwiaXNfYWRtaW4iOnRydWV9.lJ3VflMuKI2G451mz09Ty6B80CUfuhbqMVDLYozSsl4")
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + jwt_token
        }

        for i in sorted(ids_to_delete):
            resp = requests.delete(
                url=f"{URL}residual_wood/{i}",
                headers=headers
            )

            print(resp.json())

    @staticmethod
    def update_specified_rows(row_id: int, data: List[Dict]):

        payload = []

        for row in data:
            if row_id == row['id']:
                updating_row = row.copy()
                del updating_row['id']
                del updating_row['timestamp']
                payload.append(updating_row)
        print(payload[0])
        json_payload = json.dumps(payload[0])
        access_token = (
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNjk5Mzc1NDMwLCJqdGkiOiI0YTRiMD"
            "dlOS0xNTcwLTRkYjQtODE0NC1lOTk0NGE2ZDZhMDUiLCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoxLCJuYmYiOjE2OTkzNzU0"
            "MzAsImV4cCI6MTY5OTM3NjMzMCwiaXNfYWRtaW4iOnRydWV9.QMAcPDR8fOtlCfwAyl5ORtkwfl8RTo7nChR4xPgZZQE"
        )
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + access_token
        }
        resp = requests.patch(
            url=f"{URL}residual_wood/{row_id}",
            headers=headers,
            data=json_payload
        )
        print(resp.json())

    def compile_data_from_csv(self):
        df = self.data_frame
        df = df.fillna('')

        try:
            for index, row in df.iterrows():
                d = {
                    "id": int(row['id']),
                    "length": float(row['length']),
                    "name": "Red oak FSC",
                    "width": float(row['width']),
                    "height": float(row['height']),
                    "weight": float(row['weight']),
                    "color": "222,130,34",
                    "reserved": False,
                    "reservation_name": "",
                    "reservation_time": "",
                    "type": "hardwood",
                    "price": 0.0,
                    "source": "HvA Jakoba Mulderhuis (JMH)",
                    "timestamp": self.timestamp,
                    "info": row['info'],
                    "density": float(float(row['weight']) / (
                            float(row['length']) * float(row['width']) * float(row['height'])) * 1000000),
                    "storage_location": row['storage_location'],
                    "intake_id": 1
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

    # Initiating the class
    out = WoodDbManager()

    out.filter_removed_ids_from_csv()

    # compile data from the manually entered data in csv
    # out.compile_data_from_csv()

    # update rows by ids
    # for r in out.output:
    #     out.update_specified_rows(r['id'], out.output)

    # To update all the rows for correction of data
    # out.apply_correction()

    # To read and restore a backup file
    # out.restore_backup()

    # To remove rows from the database based on range of row IDs
    # out.clean_up_data(1, 101)

    # For inserting data from CSV to the DB
    # data_to_insert = out.compile_data_from_csv()
