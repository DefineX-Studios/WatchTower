import server
import windows
import mail
import time


if __name__ == '__main__':
    current_timestamp = int(time.time())
    service_status = {}
    history = {}
    process_status = {}
    dead_processes = ""
    dead_services = ""

    # Routine call
    cpu_usage = windows.get_cpu_usage()
    ram_usage = windows.get_ram_usage()
    disk_usage = windows.get_disk_usage()
    commands_list = windows.list_processes()
    server_json = server.read_from_json('server.json')

    for key, value in server_json.items():
        if key != "polling_rate":
            for key1, value1 in value['monitoring_processes'].items():
                process_status[key1] = windows.get_process_info(value1)
                if not process_status[key1]:
                    dead_processes += value1 + "\n"
            if dead_processes:
                mail.send_mail(dead_processes, 'process')

            for key1, value1 in value['monitoring_services'].items():
                service_status[key1] = windows.get_service_status(value1)
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
            history[current_timestamp][driver_letter] = (
                        (int(drive_info[1]) / 1024) / 1024 / 1024).__round__(2)

    server.write_from_json(history, "history")
