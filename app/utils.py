import json
import requests

from app import constants
from app.models import Vehicle


def fetch_from_api(vin: str) -> Vehicle:
    response = requests.get(f"{constants.API_URL}/vehicles/DecodeVin/{vin}?format=json")
    json_data = json.loads(response.content)
    vehicle = extract_from_response(vin, json_data)
    return vehicle


def extract_from_response(vin: str, payload: dict) -> Vehicle:
    result = {'vin': vin, 'cached': False}
    for element in payload.get('Results', []):
        variable = element.get('Variable', '')
        value = element.get('Value', '')
        if variable in constants.KEYS:
            variable = variable.replace(' ', '_').lower()
            result[variable] = value

    return Vehicle(**result)
