import os
import requests

"""
    To use the image upload endpoint you need to specify the ID of the wood
    as the file name, also you need to set the 'dir' parameter in the request url which indicates what directory the image will be saved in.

    For the directory to save the image in make a choice from the folders depending on your application. The options are:

        1. wood_intake: creates a folder for the images taken from the wood by the  camera (RGB images)

        2. depth_png: creates a folder for the PNG images from Triscpector
        
        3. metal_region: creates a folder for the visualization from the metal induction gate
"""

FOLDERS = ["wood_intake", "depth_png", "metal_region"]
DESTINATION = FOLDERS[0]


def upload(filepath, wood_id):
    
    try:
        assert DESTINATION in FOLDERS
    except AssertionError as err:
        print(err)

    try:

        # Check if file exists
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")

        with open(filepath, 'rb') as f:
            
            files = {'image': (filepath, f)}
            url = f"https://robotlab-residualwood.onrender.com/image/upload/{str(wood_id)}?dir={DESTINATION}"
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
        "https://robotlab-residualwood.onrender.com/login", json=credentials)

    login_response_json = login_response.json()
    token = login_response_json["access_token"]

    url = f"https://robotlab-residualwood.onrender.com/image/{str(wood_id)}?dir={DESTINATION}"
    response = requests.delete(url=url, headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    })

    print(response.json())


if __name__ == "__main__":

    # Add your own file path here for testing
    base_fp = "C:\\Users\\jjooshe\\Desktop\\wood images"
    base_filenames = []
    try:
        filenames = []
        for file in os.listdir(base_fp):
            
            filenames.append(os.path.join(base_fp, file))
            base_filenames.append(file)
        print(filenames)
        
        for i in range(len(base_filenames)):
            r = upload(filenames[i], base_filenames[i].split(".")[0])
            print(r)

        # r = upload(fp, input("Enter wood ID: "))

        # r = delete_image(
        #     input("Enter the wood ID: "),
        #     input("Username: "),
        #     input("Password: ")
        # )

    except KeyboardInterrupt:
        print('\nProgram aborted')