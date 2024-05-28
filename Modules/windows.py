import subprocess
import wmi


def get_cpu_usage():
    cpu_info = {}
    c = wmi.WMI()
    # Query CPU information
    cpu_data = c.Win32_Processor()

    # Print CPU details
    for cpu in cpu_data:
        cpu_info["name"] = cpu.Name
        cpu_info["cores"] = cpu.NumberOfLogicalProcessors
        cpu_info["load"] = cpu.LoadPercentage
        cpu_info["vtx"] = cpu.VirtualizationFirmwareEnabled

    return cpu_info


def get_ram_usage():
    available = []
    total = []
    free = []
    memory = {}

    result = subprocess.run(['wmic', 'OS', 'get', 'FreePhysicalMemory'], capture_output=True, text=True)
    if result.returncode == 0:
        free = result.stdout.split()
        memory["free"] = ((int(free[1]) / 1024).__round__())
    else:
        error_message = result.stderr.strip()
        print(f"Command execution failed with error in the function :{__name__} {error_message}")

    result = subprocess.run(['wmic', 'COMPUTERSYSTEM', 'get', 'TotalPhysicalMemory'], capture_output=True, text=True)
    if result.returncode == 0:
        total = result.stdout.split()
        memory["total"] = ((int(total[1]) / 1024) / 1024).__round__()
    else:
        error_message = result.stderr.strip()
        print(f"Command execution failed with error in the function :{__name__} {error_message}")

    if total and free:
        memory["used"] = (memory["total"] - memory["free"])
        memory["percent"] = ((memory["used"] / memory["total"]) * 100).__round__()
    else:
        error_message = 'Cannot calculate memory size'
        print(f"Command execution failed with error in the function :{__name__} {error_message}")

    return memory


def get_disk_usage():
    output = {}
    disks = []
    disk = {}
    result = subprocess.run(['wmic', 'logicaldisk', 'get', 'Name,FreeSpace,Size'], capture_output=True, text=True)
    disks = result.stdout.split()
    disks = disks[1:]

    for i in range(0, len(disks), 3):
        if i != 0:
            disk[disks[i]] = ()
            disk[disks[i]] = (((int(disks[i + 1]) / 1024) / 1024 / 1024).__round__(2),
                              ((int(disks[i - 1]) / 1024) / 1024 / 1024).__round__(2))

    return disk


def get_gpu_usage():
    #  wmic path Win32_VideoController get Name | findstr "NVIDIA"
    all_gpus = []
    nvidia_gpus = []
    amd_gpus = []

    command = 'wmic path Win32_VideoController get Name'
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode == 0:
        output = result.stdout.strip().split('\n')
        # list comprehension
        nvidia_gpus = [line.strip() for line in output if 'NVIDIA' in line]
        amd_gpus = [line.strip() for line in output if 'AMD' in line]
    else:
        error_message = result.stderr.strip()
        print(f"Command execution failed with error: {error_message}")

    if nvidia_gpus:
        # Command to retrieve NVIDIA GPU information
        command = "nvidia-smi --query-gpu=index,memory.total,memory.used," \
                  "temperature.gpu,power.draw --format=csv,noheader"

        # Execute the command and capture the output
        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode == 0:
            output = result.stdout.strip().split("\n")

            for line in output:
                n_gpu_info = line.split(", ")
                all_gpus.append(n_gpu_info)
        else:
            error_message = result.stderr.strip()
            print(f"Command execution failed with error: {error_message}")

    if amd_gpus:
        command = "rocm-smi --showmeminfo --showtemp --showpower"
        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode == 0:
            output = result.stdout.strip().split("\n")

            for line in output:
                a_gpu_info = line.split(":")
                all_gpus.append(a_gpu_info)
        else:
            error_message = result.stderr.strip()
            print(f"Command execution failed with error: {error_message}")

    return all_gpus


def list_processes(num_processes=20):
    c = wmi.WMI()
    processes = c.Win32_Process()

    # Sort the processes based on their WorkingSetSize (memory usage)
    sorted_processes = sorted(processes, key=lambda x: x.WorkingSetSize, reverse=True)

    # Get the top 'num_processes' processes
    top_processes = sorted_processes[:num_processes]

    # Create a dictionary with the specified format
    result = {}
    for process in top_processes:
        process_info = {
            "process_name": process.Name,
            "memory_used": process.WorkingSetSize
        }
        result[process.ProcessId] = process_info

    return result


def get_service_status(service_name):

    if service_name:
        service_info = {}
        c = wmi.WMI()
        services = c.Win32_Service(Name=service_name)

        if services:
            for service in services:
                service_info = {
                    'Name': service.Name,
                    'PathName': service.PathName,
                    'ProcessId': service.ProcessId,
                    'StartMode': service.StartMode,
                    'State': service.State,
                    'Status': service.Status
                }
            return tuple(service_info)
        else:
            error_message = f"Service not found ==> {service_name}"
            print(f"Command execution failed with error: {error_message}")
    else:
        error_message = "No Service name set."
        print(f"Command execution failed with error: {error_message}")

    del service_name


def get_process_info(process_name):
    if process_name:
        c = wmi.WMI()
        processes = []

        p = c.Win32_Process(Name=process_name)

        if p:
            for process in p:
                processes.append(process.ProcessId)
        else:
            error_message = f"Process not found ==> {process_name}"
            print(f"Command execution failed with error: {error_message}")

        return tuple(processes)

    else:
        error_message = "No Process name set."
        print(f"Command execution failed with error: {error_message}")

    c = None
    process_name = None


def test_command_line(command):
    return subprocess.run(command, capture_output=True, text=True)
