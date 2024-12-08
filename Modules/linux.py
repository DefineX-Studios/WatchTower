import subprocess
import psutil
import re


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


"""
Fetch and process sensor data based on the grep pattern provided.
:param grep_pattern: The grep pattern to filter sensor data (e.g., 'RPM', '°C', 'W')
:return: A list of processed sensor data in the format 'Component: Value'
"""


def get_sensor_data(grep_pattern):
    sensors_output = []
    try:
        sensors_output = subprocess.run(f'sensors | grep {grep_pattern}', capture_output=True, shell=True,
                                        check=True).stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running sensors command: {e}")
        return []

    decoded_data = sensors_output.decode('utf-8')

    array = [line.strip() for line in decoded_data.split('\n') if line.strip()]

    result = {}
    for entry in array:
        # Skip entries that start with '('
        if entry.strip().startswith('('):
            continue
        # Remove parentheses content
        cleaned_entry = re.sub(r'\(.*?\)', '', entry).strip()
        # Split into component name and value
        if ':' in cleaned_entry:
            component, value = map(str.strip, cleaned_entry.split(':', 1))
            # Extract numeric value, remove '+' if present
            number = re.search(r'[-+]?\d*\.\d+|\d+', value).group().lstrip('+')
            result[component] = number

    return result


"""
Get fan speed data.
:return: List of fan speed data
"""


def get_fan_speed():
    return get_sensor_data('RPM')


"""
Get temperature data.
:return: List of temperature data
"""


def get_temp_data():

    return get_sensor_data('°C')


"""
Get power wattage data.
:return: List of wattage data
"""


def get_wattage():
    return get_sensor_data('W')
