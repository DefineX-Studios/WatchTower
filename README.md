# WatchTower

A simplified AIO server monitor.

## Table of Contents

- [Installation](#installation)
- [Configuration Requirements](#configuration-requirements)
- [How to Run](#how-to-run)
- [License](#license)

## Installation

To install the project, follow these steps:

1. Clone the repository to your local machine:
   ```shell
   git https://github.com/DefineX-Studios/WatchTower.git
   ```

2. Place the files in the desired folder.

## Configuration Requirements

The project requires the following configuration files:

### ssh_config.json

The `ssh_config.json` file contains the SSH configuration details. Please provide the following information in the file:

```json
{
  "user": "",
  "port": 22,
  "ip": "ip_address",
  "password": "password",
  "identity": "identity_file",
  "local_path": "local_path",
  "remote_path": "remote_path"
}
```

- `"user"`: Username for SSH authentication.
- `"port"`: Port number for the SSH connection.
- `"ip"`: IP address of the server.
- `"password"`: Password for SSH authentication (optional, can be left empty if using identity key).
- `"identity"`: Path to the identity file (private key) for SSH authentication (optional, can be left empty if using password).
- `"local_path"`: Path to the local directory or file.
- `"remote_path"`: Path to the remote directory or file.

### server.json

The `server.json` file contains the server configuration details. Please provide the following information in the file:

```json
{
  "commands": {
    "app_name": "command"
  },
  "monitoring_processes": {
    "p1": "p1.exe",
    "p2": "p2.exe"
  },
  "monitoring_services": {
    "s1": "s1_name",
    "s2": "s2_name"
  },
  "polling_rate": 1,
  "max_data_history": 30
}
```

- `"commands"`: A dictionary of application names as keys and corresponding commands as values.
- `"monitoring_processes"`: A dictionary of process names as keys and their corresponding executable names as values.
- `"monitoring_services"`: A dictionary of service names as keys and their corresponding service names as values.
- `"polling_rate"`: Polling rate in minutes.

### mail_config.json

The `mail_config.json` file contains the email configuration details. Please provide the following information in the file:

```json
{
  "sender_email": "",
  "receiver_email": "",
  "smtp_server": "",
  "smtp_port": 400,
  "smtp_username": "",
  "smtp_password": ""
}
```

- `"sender_email"`: Email address of the sender.
- `"receiver_email"`: Email address of the receiver.
- `"smtp_server"`: SMTP server address.
- `"smtp_port"`: SMTP server port number.
- `"smtp_username"`: Username for SMTP server authentication.
- `"smtp_password"`: Password for SMTP server authentication.

## How to Run

To run the project:

1. Execute the cron file in the background.

## License

This project is licensed under the MIT.