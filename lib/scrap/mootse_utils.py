from logging import INFO, Formatter, StreamHandler, getLogger
from traceback import format_exc

import requests
from bs4 import BeautifulSoup

from config.config import MOOTSE_PASSWORD, MOOTSE_URL, MOOTSE_USERNAME


class MootseUtils():

    def __init__(self) -> None:
        self.logger = self.__configure_logger()
        self.mootse_username = MOOTSE_USERNAME
        self.mootse_password = MOOTSE_PASSWORD
        self.mootse_url = MOOTSE_URL

    def __configure_logger(self):
        logger = getLogger(__name__)

        if not logger.hasHandlers():
            logger.setLevel(INFO)
            formatter = Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            ch = StreamHandler()
            ch.setFormatter(formatter)
            logger.propagate = False
            logger.addHandler(ch)

        return logger

    def create_mootse_session(self):
        session = requests.Session()
        return session

    def login_to_mootse(self, session):
        self.logger.info("Connection à Mootse...")
        login_response = session.post(f"{self.mootse_url}/login/index.php")
        soup = BeautifulSoup(login_response.text, "html.parser")
        token = soup.select_one("input[name=logintoken]")["value"]
        login_data = {
            "username": self.mootse_username,
            "password": self.mootse_password,
            "logintoken": token
        }

        res = session.post(
            f"{self.mootse_url}/login/index.php", data=login_data)

        try:
            soup = BeautifulSoup(res.text, 'html.parser')
            error_message = soup.find(
                'div', {'class': 'alert alert-danger'}).text.strip()
            if error_message == "La connexion a échoué, veuillez réessayer":
                raise ConnectionError()
        except ConnectionError:
            exit(-1)
        except:
            self.logger.debug("Authentification réussie à Mootse.")

        self.logger.info("Connection à Mootse réussie.")
