import server
import windows

if __name__ == '__main__':

    cpu_usage = windows.get_cpu_usage()
    ram_usage = windows.get_ram_usage()
    disk_usage = windows.get_disk_usage()
    commands_list = windows.list_processes()
    server_json = server.read_from_json()
    service_status = {}
    process_status = {}

    for key, value in server_json.items():
        for key1, value1 in value['monitoring_processes'].items():
            process_status[key1] = windows.get_process_info(value1)

        for key1, value1 in value['monitoring_services'].items():
            service_status[key1] = windows.get_service_status(value1)

    print(cpu_usage)
    print(ram_usage)
    print(disk_usage)
    print(commands_list)
    print(process_status)
    print(service_status)
    # print(server_json)





