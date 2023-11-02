import datetime
import json

import pandas as pd
import requests


class ManualCSVDataToResidualWoodDB:
    """Follows the schema of the residual wood"""

    def __init__(
            self,
            fp: str = "../data_backup/wood database v3.1.csv",
            delimiter: str = ";",
            backup_fp: str = "./../data_backup/backup_11-02-2023.json",
            save_file: str = "../wood database v3.1.json",
            **kwargs
    ):
        self.fp = fp
        self.backup_fp = backup_fp
        self.save_file = save_file
        self.delimiter = delimiter
        self.info = kwargs.get(
            "info",
            "Intake for residual wood in Robot Lab HvA, for production of the Stool in WP1 for CW4.0 Project"
        )

        self.source = kwargs.get("source", "HvA Jakoba Mulderhuis (JMH)")
        self.price = kwargs.get("price", 0.0)
        self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M-%S")

        self.reserved = False
        self.reserved_by = "-"
        self.reserved_at = "-"

        self.color = kwargs.get("color", ["222,130,34"])
        self.wood_id = self.generate_label_from_column()
        self.output = []

    def generate_label_from_column(self) -> list:
        wood_id = self.data_frame['wood_id']
        generated_wood_ids = []
        for k, v in wood_id.items():
            label_format = '0' * (7 - len(str(v))) + str(v)
            generated_wood_ids.append(label_format)
        return generated_wood_ids

    @property
    def data_frame(self):
        return pd.read_csv(self.fp, delimiter=self.delimiter)

    @staticmethod
    def clean_db(start_index, end_index):
        for index in range(start_index, end_index + 1):
            requests.delete(url=f"https://robotlab-residualwood.onrender.com/residual_wood/{index}")

    def restore_backup(self):
        all_rows = list()

        with open(self.backup_fp, 'r') as back_up_data:
            rows = json.load(back_up_data)

            for i in range(252, len(rows)):
                del rows[i]['id']

                # del rows[i]['timestamp']
                # del rows[i]['density']
                # del rows[i]['wood_id']
                # rows[i]['density'] = 100

                rows[i]['label'] = ""
                rows[i]['reservation_name'] = ""
                rows[i]['reservation_time'] = ""

                rows[i]['paint'] = ""
                rows[i]['project_type'] = ""
                rows[i]['image'] = ""
                rows[i]['price'] = 0
                rows[i]['intake_id'] = 1
                rows[i]['wood_species'] = ""
                rows[i]['name'] = ""

                all_rows.append(rows[i])

            for r in all_rows:
                body = json.dumps(r)
                # print(body)
                requests.post(
                    url="https://robotlab-residualwood.onrender.com/residual_wood",
                    headers={'Content-Type': 'application/json'},
                    data=body
                )

    def apply_correction(self):
        existing_rows = []
        with open(self.backup_fp, 'r') as back_up_data:
            rows = json.load(back_up_data)
            for i in range(len(rows)):
                del rows[i]['timestamp']

                rows[i]['weight'] /= 10

                if rows[i]['weight'] != 0 and 0 < rows[i]['weight'] < 10:
                    rows[i]['weight'] *= 1000

                if i > 252:
                    rows[i]['weight'] *= 10

                rows[i]['source'] = "HvA Jakoba Mulderhuis (JMH)"

                try:
                    rows[i]['density'] = rows[i]['weight'] / rows[i]['length'] * rows[i]['width'] * rows[i]['height'] * 0.1
                except ZeroDivisionError:
                    rows[i]['density'] = 0

                existing_rows.append(rows[i])

            for r in existing_rows:
                print(f"ID:{r['id']}", r)

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
                "color": self.color[0],
                "reserved": self.reserved,
                "reservation_name": self.reserved_by,
                "reservation_time": self.reserved_at,
                "type": "hardwood",
                "price": self.price,
                "source": self.source,
                "timestamp": self.timestamp,
                "info": row['info'],
                "density": int((row['length'] * row['width'] * row['height']) / row['weight']),
                "wood_id": self.generate_label_from_column()[index],
                "storage_location": row['storage_location'],
                "intake_id": 1
            }
            self.output.append(d)
        return self.output


if __name__ == "__main__":
    out = ManualCSVDataToResidualWoodDB()
    data_to_insert = out.compile_data()
    out.generate_label_from_column()
    out.apply_correction()
    # out.restore_backup()

    # for data in data_to_insert:
    #     # requests.post(url='https://robotlab-residualwood.onrender.com/residual_wood', data=data)
    #     api_call(
    #         end_point="residual_wood",
    #         payload=data,
    #         method="PATCH"
    #     )

    # out.clean_db(252, 260)