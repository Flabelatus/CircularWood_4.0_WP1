import os
import sys
import inspect

import requests

from dotenv import load_dotenv
from sqlalchemy.orm import RelationshipProperty

# current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# parent_dir = os.path.dirname(os.path.dirname(current_dir))
# sys.path.insert(0, parent_dir)

from sqlalchemy import inspect


FIELDS = [
    "color",
    "density",
    "height",
    "image",
    "info",
    "length",
    "width",
    "name",
    "source",
    "weight",
    "storage_location",
    "is_fire_treated",
    "is_planed",
    "is_straight",
]

BASE_URL = "https://robotlab-residualwood.onrender.com"


def get_wood_data(wood_id):
    url = f"{BASE_URL}/wood/{wood_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching data for wood ID {wood_id}: {e}")
        return None


def filter_data(data):
    if not data:
        return {}
    return {field: value for field, value in data.items() if field in FIELDS}


def modify_metal_row(wood_id, has_metal, metal_coords):
    data = get_wood_data(wood_id)
    filtered_data = filter_data(data)

    filtered_data["has_metal"] = has_metal
    filtered_data["metal_bbox_coords"] = metal_coords

    login_response = requests.post(
        url=BASE_URL + "/login",
        json={"username": "robotlab-admin", "password": "robotlab2024"},
    )

    access_token = login_response.json()["access_token"]

    payload = filtered_data
    
    modify_response = requests.patch(
        url=BASE_URL + "/wood/" + wood_id,
        json=payload,
        headers={"Authorization": "Bearer " + access_token},
    )

    print(modify_response.json())


def get_modifiable_fields(model):
    """
    Identifies modifiable fields in a SQLAlchemy model that are not part of specified
    relationships or partial fields.
    """
    model_instance = model()
    mapper = inspect(model)

    all_columns = [
        prop.key for prop in mapper.attrs if not isinstance(prop, RelationshipProperty)
    ]

    # Assume relationship_fields and wood_partials are either methods or properties
    if callable(getattr(model_instance, "relationship_fields", None)):
        fk_relations = model_instance.relationship_fields()
    else:
        fk_relations = getattr(model_instance, "relationship_fields", [])

    if callable(getattr(model_instance, "wood_partials", None)):
        partials = model_instance.wood_partials()
    else:
        partials = getattr(model_instance, "wood_partials", [])

    # Identify modifiable fields by excluding relationships and partials
    modifiable_fields = [
        field
        for field in all_columns
        if field not in fk_relations and field not in partials
    ]

    return modifiable_fields


# if __name__ == "__main__":

#     # modify_row(input("Enter wood ID: "), bool(input("Has metal: ")), input("Metal coords: "))
