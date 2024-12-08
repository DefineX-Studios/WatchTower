import schedule
import time
import subprocess
from Modules import server

Server = server.read_from_json('/WatchTower/Configs/server.json',True)


def run_main_script():
    command = ['python', './Modules/main.py']
    subprocess.run(command)


print(fr'[START] Time: {time.strftime("%a - %d %b %Y %H:%M:%S")}.')
print(fr'[INFO] Script is schedule to run every {Server["polling_rate"]} minutes')
schedule.every(Server["polling_rate"]).minutes.do(run_main_script)

while True:
    schedule.run_pending()
    time.sleep(1)
