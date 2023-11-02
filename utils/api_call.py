from requests import request, Response


def api_call(end_point: str, payload: dict, method: str) -> Response:
    route = "http://localhost:5001" + end_point
    headers = {
        "Content-Type": "application/json",
    }
    response = request(method=method, url=route, headers=headers, json=payload)
    return response.json()


def bulk_update_call(index_list_to_update, payload):
    route = "http://localhost:5001/residual_wood/"
    for i in range(len(index_list_to_update)):
        response = request(
            method="PATCH",
            url=route + str(i + 1),
            headers={"Content-Type": "application/json"},
            json=payload[i]
        )
        print(response.json())
        print("Updated index: {0}".format(i + 1))


if __name__ == "__main__":

    resp = request(
        method="GET",
        url="http://localhost:5001/residual_wood",
        headers={"Content-Type": "application/json"}
    )

    all_wood_data = resp.json()

    for i in range(len(all_wood_data)):
        del all_wood_data[i]["reserved"]
        del all_wood_data[i]["reservation_time"]
        del all_wood_data[i]["reservation_name"]
        del all_wood_data[i]["id"]
        # del all_wood_data[i]["timestamp"]

    for i in range(12):
        # all_wood_data[i]["intake_id"] = 1
        all_wood_data[i]["source"] = "Hooidrift 129B"
        # all_wood_data[i]["name"] = "Iroko natural"
        all_wood_data[i]["price"] = 1.85

    for i in range(12, 20):
        # all_wood_data[i]["intake_id"] = 2
        all_wood_data[i]["source"] = "Jakoba Mulder Huis (JMH)"
        # all_wood_data[i]["name"] = "Moabi natural"
        all_wood_data[i]["price"] = 0.75

    for i in range(20, 31):
        # all_wood_data[i]["intake_id"] = 3
        all_wood_data[i]["source"] = "Derako International BV"
        # all_wood_data[i]["name"] = "Meranti FSC"
        all_wood_data[i]["price"] = 1.15

    for i in range(31, len(all_wood_data)):
        # all_wood_data[i]["intake_id"] = 2
        all_wood_data[i]["source"] = "Amsterdamsche Fijnhout"
        # all_wood_data[i]["name"] = "Red oak FSC"
        all_wood_data[i]["price"] = 0.35

    print(all_wood_data)

    index_list = [i for i in range(1, len(all_wood_data) + 1)]
    bulk_update_call(index_list, all_wood_data)
