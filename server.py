import json
import paramiko
import os
import logging


def read_from_json(json_name):
    # Open the JSON file
    with open(json_name, 'r') as file:
        # Load the JSON data
        data = json.load(file)
    return data


def write_from_json(data, file_name):

    file_name = f"{file_name}.json"
    file_path = os.path.dirname(os.path.abspath(__file__)) + "\\" + file_name

    if os.path.exists(file_path):
        json_data = json.dumps(data)
        with open(file_path, "r") as file:
            pre_history = json.load(file)

        pre_history["history"].update(json.loads(json_data))

        # Write the updated pre_history back to the file
        with open(file_path, "w") as file:
            json.dump(pre_history, file, indent=4)
    else:
        initial_structure = {"history": data}
        json_data = json.dumps(initial_structure)
        with open(file_path, "w") as file:
            file.write(json_data)


def connect_to_server(server_data):
    client = []
    for key, value in server_data.items():

        ip = value['ip']
        port = value['port']
        username = value['user']
        password = value['password']

        client[value['key']] = paramiko.SSHClient()
        client[value['key']].set_missing_host_key_policy(paramiko.AutoAddPolicy())

        client[value['key']].connect(ip, port, username, password)

        return client


def export_to_json(data, file_path):
    # Create the file if it doesn't exist
    with open(file_path, 'w') as file:
        # Export the data to JSON format
        json.dump(data, file, indent=4)
