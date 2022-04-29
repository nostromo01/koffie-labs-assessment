import re

API_URL = "https://vpic.nhtsa.dot.gov/api/"
VALID_VIN_REGEX = re.compile(r'^[A-HJ-NPR-Za-hj-npr-z\d]{8}[\dX][A-HJ-NPR-Za-hj-npr-z\d]{2}\d{6}$')
KEYS = ['Make', 'Model', 'Model Year', 'Body Class']
