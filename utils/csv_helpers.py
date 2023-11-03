"""
Some scripts to help overwriting data in the database for correction etc.
For further questions you can contact me: j.jooshesh@hva.nl
"""

import datetime
import json

import pandas as pd
import requests


BACKUP_FILEPATH = "./../data_backup/backup_11_03_2023.json"
CSV_FILEPATH = ""
SAVING_FILEPATH = ""


class ManualCSVDataToResidualWoodDB:
    """This class is to help manipulating the wood database according to the data in the csv format that are manually
     measuredFollows the schema of the residual wood"""

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
    def clean_db(start_index, end_index):
        for index in range(start_index, end_index + 1):
            print("Deleting row :", index, " -- Request is not sent, this is printed statement only")
            # For safety this request is commented.
            # requests.delete(url=f"https://robotlab-residualwood.onrender.com/residual_wood/{index}")

    def restore_backup(self):
        all_rows = list()

        with open(self.backup_fp, 'r') as back_up_data:
            rows = json.load(back_up_data)

            for i in range(1, len(rows)):
                del rows[i]['id']

                for j in range(len(rows)):
                    for key in rows[i]:
                        if rows[i][key] is None:
                            if key != 'price':
                                rows[i][key] = ""
                            else:
                                rows[i][key] = 0

                all_rows.append(rows[i])

            for r in all_rows:
                body = json.dumps(r)
                print(body)

                # For safety this is disabled

                # requests.post(
                #     url="https://robotlab-residualwood.onrender.com/residual_wood",
                #     headers={'Content-Type': 'application/json'},
                #     data=body
                # )

    def apply_correction(self):
        updated_rows = []
        with open(self.backup_fp, 'r') as back_up_data:
            existing_rows = json.load(back_up_data)
            for i in range(len(existing_rows)):

                # delete this field as it's not needed to update
                del existing_rows[i]['timestamp']
                existing_rows[i]['source'] = "HvA Jakoba Mulderhuis (JMH)"

                # Here you can add any changes needed to update the database
                #

                # After the changes, add them to th rows
                updated_rows.append(existing_rows[i])

        # update all the rows
        for r in updated_rows:
            new_row = r.copy()
            del new_row['id']

            payload = json.dumps(new_row)

            print(r['id'], "This is just printed statement, the request is not sent")

            # For safety this is disabled

            # requests.patch(
            #     url=f"https://robotlab-residualwood.onrender.com/residual_wood/{r['id']}",
            #     headers={'Content-Type': 'application/json'},
            #     data=payload
            # )

    def compile_data(self):
        df = self.data_frame
        df = df.fillna('')
        df['weight'] = df['weight'].astype(float) * 10

        for index, row in df.iterrows():
            d = {
                "length": row['length'],
                "name": "Red oak FSC",
                "width": row['width'],
                "height": row['height'],
                "weight": int(row['weight']),
                "color": "222,130,34",
                "reserved": False,
                "reservation_name": "",
                "reservation_time": "",
                "type": "hardwood",
                "price": 0,
                "source": "HvA Jakoba Mulderhuis (JMH)",
                "timestamp": self.timestamp,
                "info": row['info'],
                "density": int(row['weight'] / (row['length'] * row['width'] * row['height']) * 1000000),
                "storage_location": row['storage_location'],
                "intake_id": 1
            }
            self.output.append(d)
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
    out = ManualCSVDataToResidualWoodDB()

    # To update all the rows for correction of data
    # out.apply_correction()

    # To read and restore a backup file
    # out.restore_backup()

    # To remove rows from the database based on range of row IDs
    # out.clean_db(1, 459)

    # For inserting data from CSV to the DB
    # data_to_insert = out.compile_data()

