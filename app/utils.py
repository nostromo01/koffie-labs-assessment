import json
import requests

from app import constants
from app.models import Vehicle


def fetch_from_api(vin: str) -> Vehicle:
    """
    Fetches vehicle information from NHTSA API

    :param vin: Valid 17 digit character VIN
    :return: Vehicle object
    """
    response = requests.get(f"{constants.API_URL}/vehicles/DecodeVin/{vin}?format=json")
    json_data = json.loads(response.content)
    vehicle = extract_from_response(vin, json_data)
    return vehicle


def extract_from_response(vin: str, payload: dict) -> Vehicle:
    """
    Extracts relevant information from API response into a Vehicle object

    :param vin: Valid 17 character VIN
    :param payload: API Response from NHTSA API
    :return: Vehicle object
    """
    result = {'vin': vin, 'cached': False}
    for element in payload.get('Results', []):
        variable = element.get('Variable', '')
        value = element.get('Value', '')
        if variable in constants.KEYS:
            variable = variable.replace(' ', '_').lower()
            result[variable] = value

    return Vehicle(**result)
