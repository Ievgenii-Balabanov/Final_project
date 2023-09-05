import json
import requests


def get_queryset():
    warehouse = "http://127.0.0.1:8001/book/"
    data = requests.get(warehouse).json()
    return data


result = get_queryset()

with open("result.json", "w") as json_file:
    json.dump(result, json_file)
