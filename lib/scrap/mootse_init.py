from traceback import format_exc

from bs4 import BeautifulSoup

from lib.database import DatabaseConnector
from lib.scrap.mootse_utils import MootseUtils


class MootseInit(MootseUtils):
    """ Initialisation de Mootse (le moodle de Télécom Saint-Étienne) """

    def __init__(self) -> None:
        super().__init__()
        self.db = DatabaseConnector()

    def __get_all_topics(self, session):
        try:
            self.logger.info("Récupération des matières sur Mootse...")
            notes_url = f"{self.mootse_url}/grade/report/overview/index.php"
            notes_response = session.get(notes_url)
            notes_soup = BeautifulSoup(notes_response.text, "html.parser")

            tbody = notes_soup.tbody
            links = tbody.find_all("a")
            return links
        except:
            self.logger.critical("Impossible de récupérer les matières sur Mootse", exc_info=format_exc())

    def __store_topics_database(self, session, links):
        self.db.perform_healthcheck()
        self.db.setup_database()        

        for topic_record in links:
            topic_url = topic_record["href"]
            topic_name = topic_record.text
            content = session.get(topic_url)
            temp = BeautifulSoup(content.text, "html.parser")
            content = temp.tbody.text
            self.db.insert_new_topic(
                topic=topic_name,
                link=topic_url,
                content=content
            )

    def retrieve_topics(self):
        self.logger.info("Initialisation du Mootse Runner...")
        try:
            session = self.create_mootse_session()
            self.login_to_mootse(session)
        except:
            self.logger.critical(
                "Erreur lors de la connexion à Mootse.", exc_info=format_exc())
            exit(-1)

        try:
            links = self.__get_all_topics(session)
            self.__store_topics_database(session, links)
        except:
            self.logger.critical(
                "Impossible de traiter les matières de Mootse.", exc_info=format_exc())
            exit(-1)
        self.logger.info("Initialisation du Mootse Runner réussie.")
