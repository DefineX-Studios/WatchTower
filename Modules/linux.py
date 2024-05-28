import subprocess
import psutil


def get_cpu_usage():
    cpu_info = {}

    cpu_name = subprocess.check_output(['grep', 'model name', '/proc/cpuinfo'], universal_newlines=True)
    cpu_info['name'] = cpu_name.strip().split(':')[-1].strip()
    cpu_info["cores"] = psutil.cpu_count(logical=True)
    cpu_info["load"] = psutil.cpu_percent()
    cpu_flags = subprocess.check_output(['grep', 'flags', '/proc/cpuinfo'], universal_newlines=True)
    cpu_info['vtx'] = 'vmx' in cpu_flags.split()

    return cpu_info


def get_ram_usage():
    ram_info = {}

    ram = psutil.virtual_memory()
    ram_info['total'] = ram.total // (1024 ** 2)
    ram_info['available'] = ram.available // (1024 ** 2)
    ram_info['free'] = ram.free // (1024 ** 2)
    ram_info['percent'] = ram.percent

    return ram_info


def get_disk_usage():
    disk_usage = {}

    partitions = psutil.disk_partitions(all=True)
    for partition in partitions:
        if partition.fstype and '/dev' in partition.device:
            disk_info = psutil.disk_usage(partition.mountpoint)
            disk_usage[partition.device] = (
                (disk_info.free / (1024 ** 3)).__round__(2), (disk_info.total / (1024 ** 3)).__round__(2))

    return disk_usage


def list_processes():
    processes = {}

    for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
        try:
            process_info = proc.info
            pid = process_info['pid']
            name = process_info['name']
            memory_used = process_info['memory_info'].rss
            processes[pid] = (name, memory_used)
        except psutil.NoSuchProcesss:
            pass

    return processes


def get_service_status(service_name=''):

    if service_name:
        # Run the command and capture its output
        command = f'systemctl --type=service --state=running | grep {service_name}'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        # Parse the output and extract service information
        services = []
        lines = result.stdout.strip().split('\n')
        for line in lines:
            fields = line.split()
            if fields:
                service_info = {
                    'Name': fields[0],
                    'PathName': ' '.join(fields[4:]),
                    'ProcessId': None,
                    'StartMode': fields[1],
                    'State': fields[3],
                    'Status': fields[2]
                }

                services.append(service_info)
                return services

    else:
        error_message = "No Service name set."
        print(f"Command execution failed with error: {error_message}")


def get_process_info(process_name):
    if process_name:
        # Run the command and capture its output
        command = f"pgrep -f {process_name}"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        # Check if the command was successful and retrieve the process ID(s)
        if result.returncode == 0:
            process_ids = tuple(int(pid) for pid in result.stdout.strip().split('\n'))
            return process_ids

        # Return an empty tuple if no process IDs were found
        return ()
    else:
        error_message = "No Process name set."
        print(f"Command execution failed with error: {error_message}")

