import server
import windows

if __name__ == '__main__':
    # server_data = server.read_from_json()
    # client = server.connect_to_server(server_data)
    cpu_usage = windows.get_cpu_usage()
    ram_usage = windows.get_ram_usage()
    disk_usage = windows.get_disk_usage()
    gpu_usage = windows.get_gpu_usage()
    print(cpu_usage)
    print(ram_usage)
    print(disk_usage)
    print(gpu_usage)






