__author__ = "Andréa Joly"
__date__ = "31-01-2023"

from lib.scrap.mootse_init import MootseInit
from lib.scrap.mootse_runner import MootseRunner
from config.loader import load_variables

if __name__ == "__main__":
    MootseInit()
    #MootseRunner().run_check()