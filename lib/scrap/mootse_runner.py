from logging import INFO, Formatter, StreamHandler, getLogger
from traceback import format_exc

import requests
from bs4 import BeautifulSoup

from config.config import (DISCORD_WEBHOOK_URL, MAIL_PASSWORD, MAIL_PORT,
                           MAIL_RECIPIENTS, MAIL_SERVER, MAIL_USERNAME,
                           MOOTSE_PASSWORD, MOOTSE_URL, MOOTSE_USERNAME)
from lib.discord import DiscordNotifier
from lib.mail import MailNotifier


class MootseRunner():
    """ Scrapping de Mootse (le moodle de Télécom Saint-Étienne) """

    def __init__(self, path: str = "") -> None:
        self.logger = self.__configure_logger()
        self.path = path
        self.mootse_username = MOOTSE_USERNAME
        self.mootse_password = MOOTSE_PASSWORD
        self.mootse_url = MOOTSE_URL

    def __configure_logger(self):
        logger = getLogger(__name__)
        logger.setLevel(INFO)
        formatter = Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch = StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        return logger

    def __create_mootse_session(self):
        session = requests.Session()
        return session

    def __login_to_mootse(self, session):
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

    def __alert(self, subject: str) -> None:
        try:
            mail = MailNotifier(
                MAIL_USERNAME,
                MAIL_PASSWORD,
                MAIL_SERVER,
                MAIL_PORT
            )
            mail.alert(subject, MAIL_RECIPIENTS)
        except:
            self.logger.critical("Impossible d'envoyer les alertes mails.")

        try:
            discord = DiscordNotifier(DISCORD_WEBHOOK_URL)
            discord.alert(subject)
        except:
            self.logger.critical("Impossible d'envoyer l'alerte Discord.")

    def __check_for_new_notes(self, session, path):
        with open(path+'url.txt', 'r', encoding="utf-8") as f1:
            for line in f1:
                self.logger.debug(f"Récupération de l'URL : {line}.")
                parts = line.strip().split(" : ")
                temp = session.get(parts[0])
                temp = BeautifulSoup(temp.text, "html.parser")
                temp = temp.tbody
                with open(path+"pages/" + parts[1], "r", encoding="utf-8") as f2:
                    contents = f2.read()
                    if contents != str(temp):
                        self.logger.info(
                            f"Nouvelle note détectée en : {parts[1]}.")
                        with open(path+"pages/" + parts[1], "w", encoding="utf-8") as f2:
                            f2.write(str(temp))
                            self.__alert(parts[1])

    def run_check(self):
        try:
            session = self.__create_mootse_session()
            self.__login_to_mootse(session)
        except:
            self.logger.critical(
                "Erreur lors de la connexion à Mootse.", exc_info=format_exc())
            exit(-1)

        try:
            self.__check_for_new_notes(session, self.path)
        except:
            self.logger.critical(
                "Impossible de récupérer les nouvelles notes.", exc_info=format_exc())
            exit(-1)
