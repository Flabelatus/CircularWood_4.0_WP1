import os
import sys

import json

# from __init__ import logger, get_default_params


# default_params = get_default_params()

idemat_path = os.path.abspath(os.path.join(os.getcwd(), "..", "..", "idemat", "idenmat_2023_wood_simplified.json"))


class IdematClient:
    def __init__(self, name=None, path=idemat_path):
        self.path = path
        self.name = name
        self.content = None

    def _read_content(self):
        with open(self.path, "r") as idemat_json:
            self.content = json.load(idemat_json)
            return self.content

    @property
    def process(self):
        ...

    @property
    def footprint(self):
        ...

    @property
    def code(self):
        ...

    @property
    def eco_costs(self):
        ...

    @property
    def resource(self): ...

    @property
    def material(self): ...

    @property
    def carbon(self):
        ...

    def get_environmental_costs(self): ...

    def get_impact(self): ...

    def _format_fcs(self): ...