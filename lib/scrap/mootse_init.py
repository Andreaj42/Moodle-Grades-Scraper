import logging
import os

import mysql.connector
import requests
from bs4 import BeautifulSoup

from config.config import MOOTSE_PASSWORD, MOOTSE_URL, MOOTSE_USERNAME
from lib.database import DatabaseConnector


class MootseInit():
    """ Initialisation de Mootse (le moodle de Télécom Saint-Étienne) """

    def __init__(self, path: str = "") -> None:
        # Initialisation de la session
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

        # Scrapping des url des notes
        notes_url = f"{MOOTSE_URL}/grade/report/overview/index.php"
        notes_response = session.get(notes_url)
        notes_soup = BeautifulSoup(notes_response.text, "html.parser")

        # Nettoyage du scrapping
        tbody = notes_soup.tbody
        links = tbody.find_all("a")

        # Enregistrement en base
        db = DatabaseConnector()
        db.perform_healthcheck()
        db.setup_database()

        for topic_record in links:
            topic_url = topic_record["href"]
            topic_name = topic_record.text
            content = session.get(topic_url)
            temp = BeautifulSoup(content.text, "html.parser")
            content = temp.tbody.text
            db.insert_new_topic(
                topic=topic_name,
                link=topic_url,
                content=content
            )
