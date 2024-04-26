import requests

# Define the base URL of the Flask application
BASE_URL = 'http://127.0.0.1:5000'  # Update with your Flask app's URL

# Define the search parameters for the search_records endpoint
search_params = {
    'directory_name': 'Account',
    'search_key': 'AccountNo',
    'search_value': '20012'
}

# Make a GET request to the search_records endpoint
response = requests.get(f'{BASE_URL}/search_records', params=search_params)

# Check the response status code and handle accordingly
if response.status_code == 200:
    response_data = response.json()
    record_keys = response_data.get('matching_record_keys')
    if record_keys:
        print(f'Record keys match found": {record_keys}')
        print('Fetching record details:')
        for record_key in record_keys:
            # Make a GET request to the read_dataset endpoint for each record key
            read_params = {'directory_name': search_params['directory_name'], 'record_key': record_key}
            read_response = requests.get(f'{BASE_URL}/read_dataset', params=read_params)
            if read_response.status_code == 200:
                read_data = read_response.json()
                print(f'Record Key: {record_key}')
                print('Record Details:')
                for key, value in read_data['dataset'].items():
                    print(f'{key}: {value}')
                print('-' * 20)
            else:
                print(f'Error reading record with key {record_key}: {read_response.json()}')
    else:
        print('No record keys found.')
else:
    print(f'Error searching records: {response.json()}')
