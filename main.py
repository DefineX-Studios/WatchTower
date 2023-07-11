import server
import windows

if __name__ == '__main__':

    cpu_usage = windows.get_cpu_usage()
    ram_usage = windows.get_ram_usage()
    disk_usage = windows.get_disk_usage()
    commands_list = windows.list_processes()
    service_status = windows.get_service_status("Parsec")
    server_json = server.read_from_json()
    process_id = windows.get_process_info("Discord.exe")

    print(cpu_usage)
    print(ram_usage)
    print(disk_usage)
    print(commands_list)
    print(process_id)
    print(service_status)
    print(server_json)





