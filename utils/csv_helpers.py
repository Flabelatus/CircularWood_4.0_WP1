import datetime

import pandas as pd
from api_call import api_call


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

        self.lengths = None
        self.widths = None
        self.heights = None
        self.weights = None

        self.source = kwargs.get("source", "HvA Jakoba Mulderhuis (JMH)")
        self.price = kwargs.get("price", float(0))
        self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M-%S")

        if kwargs.get("type") and isinstance(kwargs.get("type"), list) and len(list) == self._len:
            self.type = kwargs.get("type")
        else:
            self.type = ["Hardwood"] * self._len

        self.reserved = True
        self.reserved_by = "Timo"
        self.reserved_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M-%S")

        self.color = kwargs.get("color", ["222,130,34"] * self._len)

        self.output = []

    @property
    def _len(self):
        return self.data_frame.__len__()

    @property
    def data_frame(self):
        return pd.read_csv(self.fp, delimiter=self.delimiter)

    def compile_data(self):
        lengths_dict = self.data_frame.to_dict()["length"]
        widths_dict = self.data_frame.to_dict()["width"]
        heights_dict = self.data_frame.to_dict()["height"]
        weights_dict = self.data_frame.to_dict()["weight"]

        self.lengths = [float(lengths_dict[k]) for k in lengths_dict]
        self.widths = [float(widths_dict[k]) for k in widths_dict]
        self.heights = [float(heights_dict[k]) for k in heights_dict]
        self.weights = [float(weights_dict[k]) * 10 for k in weights_dict]

        for i in range(self._len):
            self.output.append({
                "length": self.lengths[i],
                "width": self.widths[i],
                "height": self.heights[i],
                "weight": self.heights[i],
                "color": self.color[i],
                "reserved": self.reserved,
                "reservation_name": self.reserved_by,
                "reservation_time": self.reserved_at,
                "type": self.type[i],
                "price": self.price,
                "source": self.source,
                "timestamp": self.timestamp,
                "info": self.info,
                "density": ((self.lengths[i] * self.widths[i] * self.heights[i]) / self.weights[i]) / (10 ** 5)
            })

        return self.output


if __name__ == "__main__":
    out = ManualCSVDataToResidualWoodDB()
    data_to_insert = out.compile_data()
    print(len(data_to_insert))

    for i in range(len(data_to_insert)):
        api_call(
            end_point="residual_wood",
            payload=data_to_insert[i],
            method="POST"
        )
