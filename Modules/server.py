import json
import paramiko
import os
import tempfile
import datetime


def logger(message):
    temp_dir = tempfile.gettempdir()
    log_file = 'logfile.log'
    log_path = os.path.join(temp_dir, log_file)

    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_message = f'[{timestamp}] {message}\n'

    with open(log_path, 'a') as f:
        f.write(log_message)


def read_from_json(json_name):
    # Open the JSON file
    
    with open(os.getcwd() + json_name, 'r') as file:
        # Load the JSON data
        data = json.load(file)
    return data


feature_data = read_from_json('/Configs/feature_config.json')


def write_from_json(data, file_name, max_limit):
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)
    
    if os.path.exists(file_path):
        json_data = json.dumps(data)
        with open(file_path, "r") as file:
            pre_history = json.load(file)

        pre_history.update(json.loads(json_data))

        if len(pre_history) > max_limit:
            all_keys = list(pre_history.keys())
            del pre_history[all_keys[0]]

        # Write the updated pre_history back to the file
        with open(file_path, "w") as file:
            json.dump(pre_history, file, indent=4)
    else:
        initial_structure = data
        json_data = json.dumps(initial_structure)
        with open(file_path, "w") as file:
            file.write(json_data)


def ssh_transfer_files(local_path, remote_path):

    if not feature_data['ssh']:
        return ()

    ssh_config = read_from_json('/Configs/ssh_config.json')

    # Create an SSH client
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Use identity key if provided, otherwise use password
        if ssh_config['identity_key']:
            ssh_client.connect(ssh_config['hostname'], ssh_config['port'], ssh_config['username'], key_filename= ssh_config['identity_key'])
        else:
            ssh_client.connect(ssh_config['hostname'], ssh_config['port'], ssh_config['username'], ssh_config['password'])

        # Create an SFTP client
        sftp_client = ssh_client.open_sftp()

        # Transfer the file from local to remote
        sftp_client.put(ssh_config['local_path'] + local_path, ssh_config['remote_path'] + '/' + remote_path)

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
