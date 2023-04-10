from logging import getLogger, INFO, Formatter, StreamHandler

import requests
from bs4 import BeautifulSoup

from config.config import (DISCORD_WEBHOOK_URL, MAIL_PASSWORD, MAIL_PORT,
                           MAIL_RECIPIENTS, MAIL_SERVER, MAIL_USERNAME,
                           MOOTSE_PASSWORD, MOOTSE_URL, MOOTSE_USERNAME)
from lib.discord import DiscordNotifier
from lib.mail import MailNotifier


class MootseRunner():
    """ Scrapping de Mootse (le moodle de Télécom Saint-Étienne) """

    def __init__(self, path : str = "") -> None:
        self.logger = getLogger(__name__)
        self.logger.setLevel(INFO)
        formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch = StreamHandler()
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

        # Initialisation de la session
        self.logger.info("Connexion à Mootse...")
        session = requests.Session()
        login_response = session.post(f"{MOOTSE_URL}/login/index.php")

        # Extraction du token
        soup = BeautifulSoup(login_response.text, "html.parser")
        token = soup.select_one("input[name=logintoken]")["value"]

        # Connexion
        login_data = {
            "username": MOOTSE_USERNAME,
            "password": MOOTSE_PASSWORD,
            "logintoken": token
        }
        session.post(f"{MOOTSE_URL}/login/index.php", data=login_data)
        self.logger.info("Connexion à Mootse réussie.")

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
                        self.logger.info(f"Nouvelle note détectée en : {parts[1]}.")
                        with open(path+"pages/" + parts[1], "w", encoding="utf-8") as f2:
                            f2.write(str(temp))
                            try:
                                MailNotifier(
                                    MAIL_USERNAME,
                                    MAIL_PASSWORD,
                                    MAIL_SERVER,
                                    MAIL_PORT
                                ).alert(parts[1], MAIL_RECIPIENTS)
                            except:
                                self.logger.critical("Impossible d'envoyer les alertes mails.")

                            try:  
                                DiscordNotifier(
                                    DISCORD_WEBHOOK_URL).alert(parts[1])
                            except:
                                self.logger.critical("Impossible d'envoyer l'alerte Discord.")
