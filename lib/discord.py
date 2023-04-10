import requests
import json
from logging import getLogger, INFO, Formatter, StreamHandler

class DiscordNotifier():
    def __init__(self, webhook_url: str) -> None:
        self.webhook_url = webhook_url
        self.logger = getLogger(__name__)
        self.logger.setLevel(INFO)
        formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch = StreamHandler()
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    def __send_webhook(self, message: str) -> None:
        headers = {"Content-Type": "application/json"}
        response = requests.post(self.webhook_url,
                                 data=json.dumps(message),
                                 headers=headers)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise Exception(f"Une erreur s'est produite : {err}") from err

    def alert(self, subject: str) -> None:
        message = {
            "content": f"""📝 @everyone : Nouvelle note disponible sur Mootse en {subject}. Il peut s'agir d'une modification ou d'un ajout ⚠️."""}
        try:
            self.__send_webhook(message)
            self.logger.info("Notification Discord envoyée.")
        except Exception as err:
            self.logger.exception(
                f"Une erreur s'est produite lors de l'envoi de la notification Discord : {err}")
