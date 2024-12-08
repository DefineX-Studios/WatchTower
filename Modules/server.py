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


def read_from_json(json_name, modules=False):
    # Open the JSON file
    path = os.getcwd()

    if modules:
        path = os.path.abspath(os.path.join(path, ".."))

    with open(path + json_name, 'r') as file:
        # Load the JSON data
        data = json.load(file)
    return data


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
            ssh_client.connect(ssh_config['hostname'], ssh_config['port'], ssh_config['username'],
                               key_filename=ssh_config['identity_key'])
        else:
            ssh_client.connect(ssh_config['hostname'], ssh_config['port'], ssh_config['username'],
                               ssh_config['password'])

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


"""
Monitor if a website is up and measure its response time.
:param url: The URL of the website to monitor.
:param timeout: Maximum time to wait for a response (in seconds).
:return: A tuple (status, response_time) where:
         - status: 'UP' if the website is reachable, otherwise 'DOWN'
         - response_time: Response time in milliseconds (None if site is down)
"""


def monitor_website(url, timeout=5):
    import time
    import requests

    try:
        start_time = time.time()
        response = requests.get(url, timeout=timeout)
        response_time = (time.time() - start_time) * 1000

        if response.status_code == 200:
            return "UP", round(response_time, 2)
        else:
            return "DOWN", None
    except requests.exceptions.RequestException:
        return "DOWN", None


def websites_status():

    status = {}
    for website in server_data['websites']:
        status[server_data['websites'][website]] = monitor_website(server_data['websites'][website])
        export_to_json(status, 'website_status.json')


feature_data = read_from_json('/WatchTower/Configs/feature_config.json', True)
server_data = read_from_json('/WatchTower/Configs/server.json', True)