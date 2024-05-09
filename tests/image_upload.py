import os
import requests

# Make a choice depending on your case
FOLDERS = ["wood_intake", "depth_png", "metal_region", "pcd"]
DESTINATION = FOLDERS[0]


def upload(filepath, wood_id):
    try:

        # Check if file exists
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")

        with open(filepath, 'rb') as f:

            files = {'image': (filepath, f)}
            url = f"http://localhost:5050/image/upload/{str(wood_id)}?dir={DESTINATION}"
            response = requests.post(url, files=files)
            return response.json()

    except Exception as e:
        print(f"Upload failed: {str(e)}")
        return {'error': True, 'message': str(e)}


def delete_image(wood_id, username, password):

    # Robotlab account credentials needed since the route is protected
    credentials = {
        "username": username,
        "password": password
    }

    login_response = requests.post(
        "http://localhost:5050/login", json=credentials)

    login_response_json = login_response.json()
    token = login_response_json["access_token"]

    url = f"http://localhost:5050/image/{str(wood_id)}?dir={DESTINATION}"
    response = requests.delete(url=url, headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    })

    print(response.json())


if __name__ == "__main__":
    fp = "/Users/javid/Desktop/1.png"

    # r = upload(fp, input("Enter wood ID: "))

    r = delete_image(
        input("Enter the wood ID: "),
        input("Username: "),
        input("Password: ")
    )
