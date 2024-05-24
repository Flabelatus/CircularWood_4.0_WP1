import requests
import os
from dotenv import load_dotenv

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
    "is_straight"
]

BASE_URL = 'https://robotlab-residualwood.onrender.com'


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

    login_response = requests.post(url=BASE_URL + "/login", json={
        "username": "robotlab-admin",
        "password": "robotlab2024"
    })

    access_token = login_response.json()["access_token"]
    
    payload = filtered_data
    modify_response = requests.patch(url=BASE_URL + "/wood/" + wood_id, json=payload, headers={
        "Authorization": "Bearer " + access_token
    })

    print(modify_response.json())


if __name__ == "__main__":

    modify_row(input("Enter wood ID: "), bool(input("Has metal: ")), input("Metal coords: "))