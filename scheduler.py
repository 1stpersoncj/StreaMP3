import schedule
import time
import subprocess

class Scheduler:
    def __init__(self, script='main.py'):
        self.script = script

    def schedule_daily(self):
        schedule.every().day.at("02:00").do(self.run_script)
        while True:
            schedule.run_pending()
            time.sleep(1)

    def run_script(self):
        subprocess.run(["python", self.script])
