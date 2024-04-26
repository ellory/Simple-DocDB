from flask import Flask, request, jsonify
import json
import os
import uuid

app = Flask(__name__)

# Define the path where the datasets will be stored
DATASETS_DIR = 'datasets'

# Endpoint for writing a JSON dataset to a directory with a generated UUID as the record key
@app.route('/write_dataset', methods=['POST'])
def write_dataset():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No JSON data provided'}), 400

    directory_name = data.get('directory_name')
    dataset = data.get('dataset')

    if not directory_name:
        return jsonify({'error': 'Missing directory_name in JSON data'}), 400

    if not dataset:
        return jsonify({'error': 'Missing dataset in JSON data'}), 400

    # Generate a UUID as the record key
    record_key = str(uuid.uuid4())

    # Create the directory if it doesn't exist
    directory_path = os.path.join(DATASETS_DIR, directory_name)
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    file_path = os.path.join(directory_path, f'{record_key}.json')

    with open(file_path, 'w') as file:
        json.dump(dataset, file)

    return jsonify({'success': True, 'record_key': record_key}), 200

# Endpoint for reading a JSON dataset from a directory using the record key
@app.route('/read_dataset', methods=['GET'])
def read_dataset():
    directory_name = request.args.get('directory_name')
    record_key = request.args.get('record_key')

    if not directory_name:
        return jsonify({'error': 'Missing directory_name parameter'}), 400

    if not record_key:
        return jsonify({'error': 'Missing record_key parameter'}), 400

    directory_path = os.path.join(DATASETS_DIR, directory_name)
    file_path = os.path.join(directory_path, f'{record_key}.json')

    if not os.path.exists(file_path):
        return jsonify({'error': 'Dataset not found'}), 404

    with open(file_path, 'r') as file:
        dataset = json.load(file)

    return jsonify({'dataset': dataset}), 200


# Endpoint for searching for JSON files based on a JSON key and its value in a specified directory
@app.route('/search_records', methods=['GET'])
def search_records():
    directory_name = request.args.get('directory_name')
    search_key = request.args.get('search_key')
    search_value = request.args.get('search_value')


    if not search_key or not search_value or not directory_name:
        return jsonify({'error': 'Missing search_key, search_value, or directory_name in JSON data'}), 400

    directory_path = os.path.join(DATASETS_DIR, directory_name)

    if not os.path.exists(directory_path) or not os.path.isdir(directory_path):
        return jsonify({'error': 'Directory not found'}), 404

    matching_record_keys = []

    for filename in os.listdir(directory_path):
        if filename.endswith('.json'):
            file_path = os.path.join(directory_path, filename)
            with open(file_path, 'r') as file:
                file_data = json.load(file)
                if search_key in file_data and file_data[search_key] == search_value:
                    matching_record_keys.append(os.path.splitext(filename)[0])

    return jsonify({'matching_record_keys': matching_record_keys}), 200

# Endpoint for getting all directory names in the datasets directory
@app.route('/get_datasets', methods=['GET'])
def get_datasets():
    datasets = []

    if not os.path.exists(DATASETS_DIR):
        return jsonify({'datasets': datasets}), 200

    for item in os.listdir(DATASETS_DIR):
        item_path = os.path.join(DATASETS_DIR, item)
        if os.path.isdir(item_path):
            datasets.append(item)

    return jsonify({'datasets': datasets}), 200


if __name__ == '__main__':
    app.run(debug=True)
