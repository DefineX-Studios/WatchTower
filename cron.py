import schedule
import time
import subprocess
from Modules import server

server = server.read_from_json('/Configs/server.json')


def run_main_script():
    command = ['python', './Modules/main.py']
    subprocess.run(command)


print(fr'[START] Time: {time.strftime("%a - %d %b %Y %H:%M:%S")}.')
print(fr'[INFO] Script is schedule to run every {server["polling_rate"]} minutes')
schedule.every(server["polling_rate"]).minutes.do(run_main_script)

while True:
    schedule.run_pending()
    time.sleep(1)
