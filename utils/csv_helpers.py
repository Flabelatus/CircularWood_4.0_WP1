import datetime
import json

import pandas as pd
import requests

from utils.api_call import api_call


class ManualCSVDataToResidualWoodDB:
    """Follows the schema of the residual wood"""

    def __init__(
            self,
            fp: str = "../csv_data/wood database v3.1.csv",
            delimiter: str = ";",
            save_file: str = "../wood database v3.1.json",
            **kwargs
    ):
        self.fp = fp
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
    def clean_db(last_index):
        for index in range(1, last_index + 1):
            requests.delete(url=f"https://robotlab-residualwood.onrender.com/residual_wood/{index}")

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
    #
    for data in data_to_insert:
        # requests.post(url='https://robotlab-residualwood.onrender.com/residual_wood', data=data)
        api_call(
            end_point="residual_wood",
            payload=data,
            method="POST"
        )

    # out.clean_db(40)