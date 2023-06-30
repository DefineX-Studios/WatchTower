import subprocess


def get_cpu_usage():
    result = subprocess.run(['wmic', 'cpu', 'get', 'loadpercentage'], capture_output=True, text=True)
    output = result.stdout.split()

    return output


def get_ram_usage():
    available = []

    result = subprocess.run(['wmic', 'OS', 'get', 'FreePhysicalMemory'], capture_output=True, text=True)
    free = result.stdout.split()
    free[1] = (int(free[1]) / 1024).__round__(2)

    result = subprocess.run(['wmic', 'COMPUTERSYSTEM', 'get', 'TotalPhysicalMemory'], capture_output=True, text=True)
    total = result.stdout.split()
    total[1] = ((int(total[1])/1024)/1024).__round__(2)

    available.append('Available Memory')
    available.append((total[1] - free[1]).__round__(2))

    memory = [total, free, available]

    return memory


def get_disk_usage():
    # wmic logicaldisk get FreeSpace,Size,Name
    result = subprocess.run(['wmic', 'logicaldisk', 'get', 'FreeSpace,Size,Name'], capture_output=True, text=True)
    output = result.stdout.split()
    return output


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
