import datetime
import pandas as pd

from utils.api_call import api_call


class ManualCSVDataToResidualWoodDB:
    """Follows the schema of the residual wood"""

    def __init__(
            self,
            fp: str = "../csv_data/CW4_0.csv",
            delimiter: str = ";",
            save_file: str = "../csv_data/CW4_0.json",
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
        self.price = kwargs.get("price", 0)
        self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M-%S")

        self.reserved = True
        self.reserved_by = "Timo"
        self.reserved_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M-%S")

        self.color = kwargs.get("color", ["222,130,34"])

        self.output = []

    @property
    def data_frame(self):
        return pd.read_csv(self.fp, delimiter=self.delimiter)

    def compile_data(self):
        df = self.data_frame
        df['weight'] = df['weight'].astype(float) * 10

        for _, row in df.iterrows():
            d = {
                "length": float(row['length']),
                "width": float(row['width']),
                "height": float(row['height']),
                "weight": float(row['weight']),
                "color": self.color[0],
                "reserved": self.reserved,
                "reservation_name": self.reserved_by,
                "reservation_time": self.reserved_at,
                "type": "Hardwood",
                "price": self.price,
                "source": self.source,
                "timestamp": self.timestamp,
                "info": self.info,
                "density": ((row['length'] * row['width'] * row['height']) / row['weight']) / 1000
            }
            self.output.append(d)

        return self.output


if __name__ == "__main__":
    out = ManualCSVDataToResidualWoodDB()
    data_to_insert = out.compile_data()

    for data in data_to_insert:
        api_call(
            end_point="residual_wood",
            payload=data,
            method="POST"
        )
