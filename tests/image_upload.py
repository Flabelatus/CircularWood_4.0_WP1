import os
import requests


def upload(filename):
    try:
        print(f"Using filename: {filename}")  # Debugging check

        # Check if file exists
        if not os.path.exists(filename):
            raise FileNotFoundError(f"File not found: {filename}")

        with open(filename, 'rb') as f:
                    
            files = {'image': (filename, f)}
            url = "http://localhost:5050/image/upload"
            response = requests.post(url, files=files)
            return response.json()

    except Exception as e:
        print(f"Upload failed: {str(e)}")
        return {'error': True, 'message': str(e)}


if __name__ == "__main__":
    fp = "C:\\Users\\jjooshe\\Desktop\\1.jpg"
    r = upload(fp)
    print(r)
