from lib.scrap.mootse_init import MootseInit
from lib.scrap.mootse_runner import MootseRunner
from lib.database import DatabaseConnector

def do_check():
    db = DatabaseConnector()
    if(db.check_if_not_exists()): 
        MootseInit().retrieve_topics()
    else:
       MootseRunner().run_check()