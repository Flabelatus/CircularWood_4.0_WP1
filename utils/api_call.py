from requests import request, Response


def api_call(end_point: str, payload: dict, method: str) -> Response:
    route = "http://localhost:5000/" + end_point
    headers = {
        "Content-Type": "application/json",
    }
    response = request(method=method, url=route, headers=headers, json=payload)
    return response.json()


