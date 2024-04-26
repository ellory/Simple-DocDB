import requests
import json

# Define the base URL of the Flask application
BASE_URL = 'http://127.0.0.1:5000'  # Update with your Flask app's URL

# Define the JSON data to be sent to the write_dataset endpoint
data = {
    'directory_name': 'Account',
    'dataset': {
        'AccountNo': '20012',
        'Name': 'Jimmy Jones',
        'PhoneNo': 'jj@test.com',
        'Address': '1000 Calamar St., Los Angeles, CA 92122',
        'Comment': 'Savings, Checking, and Home Loan'
    }
}

# Make a POST request to the write_dataset endpoint
response = requests.post(f'{BASE_URL}/write_dataset', json=data)

# Check the response status code and handle accordingly
if response.status_code == 200:
    response_data = response.json()
    record_key = response_data.get('record_key')
    print(f'Record created successfully with record_key: {record_key}')
else:
    print(f'Error: {response.json()}')
