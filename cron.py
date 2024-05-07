import schedule
import time
import subprocess
import server

server = server.read_from_json('server.json')


def run_main_script():
    command = ['python', 'main.py']
    subprocess.run(command)


print(fr'[START] Time: {time.strftime("%H:%M:%S")}.')
print(fr'[INFO] Script is schedule to run every {server["polling_rate"]} minutes')
schedule.every(server["polling_rate"]).minutes.do(run_main_script)

while True:
    schedule.run_pending()
    time.sleep(1)
