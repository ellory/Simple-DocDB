import requests
import json

# Define the base URL of the Flask application
BASE_URL = 'http://127.0.0.1:5000'  # Update with your Flask app's URL

# Define the query parameters for the search_records endpoint
params = {
    'directory_name': 'Person',
    'search_key': 'lastname',
    'search_value': 'Smith'
}

# Make a GET request to the search_records endpoint
response = requests.get(f'{BASE_URL}/search_records', params=params)

# Check the response status code and handle accordingly
if response.status_code == 200:
    response_data = response.json()
    matching_record_keys = response_data.get('matching_record_keys')
    print(f'Records found with lastname="Smith": {matching_record_keys}')
else:
    print(f'Error: {response.json()}')
