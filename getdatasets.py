import requests

# Define the URL of the Flask server hosting the /get_datasets endpoint
server_url = 'http://127.0.0.1:5000/get_datasets'  # Update this URL if your server is running elsewhere

# Make a GET request to the /get_datasets endpoint
response = requests.get(server_url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the JSON response to get the list of datasets
    datasets = response.json().get('datasets')

    if datasets:
        print("List of datasets in 'datasets' directory:")
        for dataset in datasets:
            print(dataset)
    else:
        print("No datasets found in 'datasets' directory.")
else:
    print(f"Error: Failed to fetch datasets. Status code: {response.status_code}")
