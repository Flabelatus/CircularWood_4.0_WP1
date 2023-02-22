import os
from requests import request
from load_dotenv import load_dotenv

load_dotenv()


def api_call(end_point: str, payload: dict, method: str):
    route = os.environ["URL"] + end_point
    headers = {
        "Content-Type": "application/json",
    }
    response = request(method=method, url=route, headers=headers, json=payload)
    return {
        "message": response.json(),
        "code": response.status_code
    }

