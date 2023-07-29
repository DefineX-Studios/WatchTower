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

    file_path = os.path.dirname(os.path.abspath(__file__)) + "\\" + file_name

    if os.path.exists(file_path):
        json_data = json.dumps(data)
        with open(file_path, "r") as file:
            pre_history = json.load(file)

        pre_history.update(json.loads(json_data))

        # Write the updated pre_history back to the file
        with open(file_path, "w") as file:
            json.dump(pre_history, file, indent=4)
    else:
        initial_structure = data
        json_data = json.dumps(initial_structure)
        with open(file_path, "w") as file:
            file.write(json_data)


def ssh_transfer_files(hostname, port, username, password, local_path, remote_path, identity_key=None):
    # Create an SSH client
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Use identity key if provided, otherwise use password
        if identity_key:
            ssh_client.connect(hostname, port, username, key_filename=identity_key)
        else:
            ssh_client.connect(hostname, port, username, password)

        # Create an SFTP client
        sftp_client = ssh_client.open_sftp()

        # Transfer the file from local to remote
        sftp_client.put(local_path, remote_path)

        # Close the SFTP client
        sftp_client.close()

    finally:
        # Close the SSH client
        ssh_client.close()


def export_to_json(data, file_path):
    # Create the file if it doesn't exist
    with open(file_path, 'w') as file:
        # Export the data to JSON format
        json.dump(data, file, indent=4)
