import json
import paramiko


def read_from_json():
    # Open the JSON file
    with open('server.json', 'r') as file:
        # Load the JSON data
        data = json.load(file)

    return data


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


