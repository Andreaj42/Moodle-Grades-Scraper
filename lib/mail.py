import smtplib
import traceback
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from logging import getLogger, INFO, Formatter, StreamHandler
from typing import List

class MailNotifier():
    def __init__(self, smtp_username: str, smtp_password: str, smtp_server: str, smtp_port: int) -> None:
        self.__smtp_username = smtp_username
        self.__smtp_password = smtp_password
        self.__smtp_server = smtp_server
        self.__smtp_port = smtp_port
        self.logger = getLogger(__name__)
        self.logger.setLevel(INFO)
        formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch = StreamHandler()
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)
        
    def __send_mail(self, msg: MIMEMultipart, recipient: str) -> None:
        try:
            server = smtplib.SMTP(self.__smtp_server, self.__smtp_port)
            server.connect(self.__smtp_server, self.__smtp_port)
            server.starttls()
            server.ehlo()
            server.login(self.__smtp_username, self.__smtp_password)
            server.sendmail(self.__smtp_username, recipient, msg.as_string())
            server.quit()
        except Exception as e:
            self.logger.exception("Erreur lors de l'envoi du mail à l'adresse : " + recipient)

    def __forge_mail(self, subject: str, recipient: str):
        event_html = f"""
            <div class="event-container">
                <div class="event-details">
                    <h2>Matière concernée : {subject}</h2>
                </div>
            </div>
        """
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"Mootse : Nouvelle note en {subject}"
        msg['From'] = formataddr(("Mootse Runner", self.__smtp_username))
        msg['To'] = recipient
        html_content = """
        <html>
            <head>
                <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
                <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
                <style>
                    /* Email styles */
                    @media only screen and (max-width: 600px) {
                        .email-container {
                            width: 100% !important;
                            padding: 0 !important;
                        }
                        .email-body {
                            padding: 20px !important;
                        }
                    }

                    /* Body styles */
                    body {
                        margin: 0;
                        padding: 0;
                        font-family: Arial, sans-serif;
                        font-size: 16px;
                        color: #444444;
                    }

                    /* Container styles */
                    .email-container {
                        width: 100%;
                        max-width: 600px;
                        margin: 0 auto;
                        background-color: #f9f9f9;
                        padding: 20px;
                        border-radius: 10px;
                    }

                    /* Header styles */
                    .email-header {
                        background-color: #005EA6;
                        color: white;
                        padding: 10px;
                        border-radius: 10px 10px 0 0;
                    }

                    /* Content styles */
                    .email-content {
                        background-color: #ffffff;
                        padding: 20px;
                        border-radius: 0 0 10px 10px;
                    }

                    /* Footer styles */
                    .email-footer {
                        background-color: #f9f9f9;
                        color: #999999;
                        padding: 10px;
                        border-radius: 0 0 10px 10px;
                    }

                    /* Event styles */
                    .event-container {
                        margin-top: 20px;
                        border: 1px solid #dcdcdc;
                        padding: 10px;
                        border-radius: 5px;
                    }

                    .event-title {
                        font-weight: bold;
                    }

                    .event-dates {
                        margin-top: 10px;
                    }
                </style>
            </head>
            """
        html_content += """
                    <body>
                        <div class="email-container">
                        <div class="email-header">
                            <h1 style="margin: 0;">Alerte - Mootse</h1>
                        </div>
                        <div class="email-content">
                            <h3 style="margin: 0;">Une nouvelle note est disponible sur Mootse.
                            Il peut s'agir d'une modification ou d'un ajout !</h3>
                            {event_html}
                        </div>
                        <div class="email-footer">
                            <p style="margin: 0;">Ceci est un mail automatique. Merci de ne pas répondre.</p>
                        </div>
                    </body>
                </html>
                    """.format(event_html=event_html)
        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)
        self.__send_mail(msg, recipient)
        self.logger.info("Mail envoyé avec succès à l'adresse : " + recipient)
    
    def alert(self, subject: str, recipients: List[str]):
        for recipient in recipients:
            self.__forge_mail(subject, recipient)