import subprocess
import wmi


def get_cpu_usage():
    cpu_info = []
    c = wmi.WMI()
    # Query CPU information
    cpu_data = c.Win32_Processor()

    # Print CPU details
    for cpu in cpu_data:
        cpu_info.append(cpu.Name)
        cpu_info.append(cpu.NumberOfLogicalProcessors)
        cpu_info.append(cpu.LoadPercentage)
        cpu_info.append(cpu.VirtualizationFirmwareEnabled)

    return cpu_info


def get_ram_usage():
    available = []
    total = []
    free = []
    memory = {}

    result = subprocess.run(['wmic', 'OS', 'get', 'FreePhysicalMemory'], capture_output=True, text=True)
    if result.returncode == 0:
        free = result.stdout.split()
        memory[free[0]] = ((int(free[1]) / 1024).__round__(2))
    else:
        error_message = result.stderr.strip()
        print(f"Command execution failed with error in the function :{__name__} {error_message}")

    result = subprocess.run(['wmic', 'COMPUTERSYSTEM', 'get', 'TotalPhysicalMemory'], capture_output=True, text=True)
    if result.returncode == 0:
        total = result.stdout.split()
        memory[total[0]] = ((int(total[1]) / 1024).__round__())
    else:
        error_message = result.stderr.strip()
        print(f"Command execution failed with error in the function :{__name__} {error_message}")

    if total and free:
        memory['Available Memory'] = ((int(total[1]) - int(free[1])).__round__())
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
            disk[disks[i]] = (disks[i + 1], disks[i - 1])

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


def list_processes():
    columns = []
    command = "tasklist"
    output = []
    result = subprocess.run(command, capture_output=True, text=True)
    # split
    output = result.stdout.split("\n")
    # let's get rid of the first two lines as they are just header
    output = output[4:]
    process_dict = {}

    # Iterate over the processes and store them in the dictionary
    for process in output:
        # Split the process information into individual columns
        columns = process.split()
        if columns:
            process_dict[columns[1]] = (columns[0], columns[4])

    return process_dict


def get_service_status(service_name):
    service_info = []
    c = wmi.WMI()
    services = c.Win32_Service(Name=service_name)

    if services:
        for service in services:
            service_info.append(service.Name)
            service_info.append(service.PathName)
            service_info.append(service.ProcessId)
            service_info.append(service.StartMode)
            service_info.append(service.State)
            service_info.append(service.Status)
    else:
        print("Service not found")

    del service_name
    return tuple(service_info)


def get_process_info(process_name):
    c = wmi.WMI()
    process = []
    for s in c.Win32_Process(Name=process_name):
        process.append(s.ProcessId)

    return tuple(process)


def test_command_line(command):
    return subprocess.run(command, capture_output=True, text=True)
