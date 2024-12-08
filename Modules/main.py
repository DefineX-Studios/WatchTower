import json
import time
import sys
import socket
import server
import mail

feature_data = server.read_from_json('/Configs/feature_config.json')


def show_progress(message, custom="[INFO]"):
    if feature_data['log']:
        print(custom + message)


if __name__ == '__main__':
    show_progress("Starting script...")
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

    show_progress("Gathering system information...")
    cpu_usage = module.get_cpu_usage()
    ram_usage = module.get_ram_usage()
    disk_usage = module.get_disk_usage()
    commands_list = module.list_processes()
    temp_stats = module.get_temp_data()
    fan_stats = module.get_fan_speed()
    wattage_stat = module.get_wattage()
    server_json = server.read_from_json('/Configs/server.json')
    live_data.append(cpu_usage)
    live_data.append(ram_usage)
    live_data.append(disk_usage)
    live_data.append(commands_list)

    show_progress("Checking monitored processes...")
    if server_json['monitoring_processes']:
        for key1, value1 in server_json['monitoring_processes'].items():
            process_status[key1] = module.get_process_info(value1)

            if not process_status[key1]:
                dead_processes += value1 + "\n"

            if dead_processes:
                mail.send_mail(dead_processes, 'process')

    show_progress("Checking monitored services...")
    if server_json['monitoring_services']:
        for key1, value1 in server_json['monitoring_services'].items():
            service_status[key1] = module.get_service_status(value1)

            if not service_status[key1]:
                dead_services += value1 + "\n"

        if dead_services:
            mail.send_mail(dead_services, 'service')

    show_progress("Saving system history...")
    history = {current_timestamp: {}}

    if cpu_usage:
        history[current_timestamp]['cpu_used'] = cpu_usage['load']

    if ram_usage:
        history[current_timestamp]['ram_used'] = ram_usage['percent']

    if disk_usage:
        for driver_letter, drive_info in disk_usage.items():
            history[current_timestamp][driver_letter] = (drive_info[1])

    if fan_stats:
        history[current_timestamp]['fan'] = fan_stats

    if temp_stats:
        history[current_timestamp]['temp'] = temp_stats

    if wattage_stat:
        history[current_timestamp]['watts'] = wattage_stat

    history_file = socket.gethostname() + '-history.json'
    live_file = socket.gethostname() + '-current.json'

    server.write_from_json(history, history_file, server_json["max_data_history"])
    server.export_to_json(live_data, live_file)

    show_progress("Transferring files via SSH...")
    server.ssh_transfer_files(history_file, history_file)
    server.ssh_transfer_files(live_file, live_file)
    show_progress("Saving system history...")

    server.websites_status()

    show_progress("Script completed successfully.", "[END]")
