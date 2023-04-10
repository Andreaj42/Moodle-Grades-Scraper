import requests
import json


class DiscordNotifier():
    def __init__(self, webhook_url: str) -> None:
        self.webhook_url = webhook_url

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
        except Exception as err:
            raise Exception(
                f"Une erreur s'est produite lors de l'envoi de la notification Discord : {err}") from err
