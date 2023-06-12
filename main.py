__author__ = "Andréa Joly"
__date__ = "31-01-2023"

from apscheduler.schedulers.blocking import BlockingScheduler

from config.config import SCAN_INTERVAL
from lib.check import do_check

if __name__ == "__main__":
    scheduler = BlockingScheduler(timezone='Europe/Paris')
    scheduler.add_job(do_check, "interval", seconds=SCAN_INTERVAL)
    scheduler.start()
