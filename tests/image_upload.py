import os
import requests


def upload(filepath, wood_id):
    try:

        # Check if file exists
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")

        with open(filepath, 'rb') as f:
                    
            files = {'image': (filepath, f)}
            url = f"http://localhost:5050/image/upload/{str(wood_id)}"
            response = requests.post(url, files=files)
            return response.json()

    except Exception as e:
        print(f"Upload failed: {str(e)}")
        return {'error': True, 'message': str(e)}


if __name__ == "__main__":
    fp = "C:\\Users\\jjooshe\\Desktop\\1.jpg"
    r = upload(fp, input("Enter the wood ID: "))
    print(r)
