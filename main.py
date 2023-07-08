import server
import windows

if __name__ == '__main__':

    cpu_usage = windows.get_cpu_usage()
    ram_usage = windows.get_ram_usage()
    disk_usage = windows.get_disk_usage()
    commands_list = windows.list_processes()

    print(cpu_usage)
    print(ram_usage)
    print(disk_usage)
    print(commands_list)





