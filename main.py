import server
import mail
import time
import sys
import socket


if __name__ == '__main__':
    current_timestamp = int(time.time())
    service_status = {}
    history = {}
    process_status = {}
    dead_processes = ""
    dead_services = ""
    live_data = []

    if sys.platform.startswith('win'):
        # Import modules for Windows
        import windows as module
    elif sys.platform.startswith('linux'):
        # Import modules for Linux
        import linux as module
    else:
        # Handle unsupported operating system
        print("Unsupported operating system")
        sys.exit(1)

    # Routine call
    cpu_usage = module.get_cpu_usage()
    ram_usage = module.get_ram_usage()
    disk_usage = module.get_disk_usage()
    commands_list = module.list_processes()
    server_json = server.read_from_json('server.json')
    ssh_config = server.read_from_json('ssh_config.json')

    live_data.append(cpu_usage)
    live_data.append(ram_usage)
    live_data.append(disk_usage)
    live_data.append(commands_list)

    if server_json['monitoring_processes']:
        for key1, value1 in server_json['monitoring_processes'].items():
            process_status[key1] = module.get_process_info(value1)

            if not process_status[key1]:
                dead_processes += value1 + "\n"

            if dead_processes:
                mail.send_mail(dead_processes, 'process')

    if server_json['monitoring_services']:
        for key1, value1 in server_json['monitoring_services'].items():
            service_status[key1] = module.get_service_status(value1)

            if not service_status[key1]:
                dead_services += value1 + "\n"

        if dead_services:
            mail.send_mail(dead_services, 'service')

    history = {current_timestamp: {}}

    if cpu_usage:
        history[current_timestamp]['cpu_used'] = cpu_usage['load']

    if ram_usage:
        history[current_timestamp]['ram_used'] = ram_usage['percent']

    if disk_usage:
        for driver_letter, drive_info in disk_usage.items():
            history[current_timestamp][driver_letter] = (drive_info[1])

    history_file = socket.gethostname() + '-history.json'
    live_file = socket.gethostname() + '-live.json'

    server.write_from_json(history, history_file)
    server.export_to_json(live_data, live_file)

    # hostname, port, username, password, local_path, remote_path, identity_key=None

    server.ssh_transfer_files(ssh_config['ip'], ssh_config['port'], ssh_config['user'], ssh_config['password'],
                              ssh_config['local_path'] + history_file, ssh_config['remote_path'] + '/' + history_file,
                              ssh_config['identity'])

    server.ssh_transfer_files(ssh_config['ip'], ssh_config['port'], ssh_config['user'], ssh_config['password'],
                              ssh_config['local_path'] + live_file, ssh_config['remote_path'] + '/' + live_file,
                              ssh_config['identity'])

