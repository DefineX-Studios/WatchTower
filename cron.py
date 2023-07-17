import schedule
import time
import subprocess
import server

print("Process started")
server = server.read_from_json('server.json')


def run_main_script():
    command = ['python', 'main.py']
    subprocess.run(command)


schedule.every(server["polling_rate"]).minutes.do(run_main_script)

while True:
    schedule.run_pending()
    time.sleep(1)
