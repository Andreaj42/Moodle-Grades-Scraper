import smtplib
import traceback
from logging import getLogger


def alert(matiere, path):
    logger = getLogger()
    sender = "poubelleproust@perfeito.fr"
    receiver_email = []
    password = "|nONQXlkbroKwz![HPc5~D=*EUB7Hd(N:tu1]Qj"
    try:
        with open(path+"mail.txt", "r") as f:
            for line in f:
                receiver_email.append(line)
        msg = f"""\
From: {sender}
Subject: Mootse : Nouvelle note en {matiere}

Une note a été ajoutée en {matiere}, 
Ce message peut s'agir d'une modification ou d'un ajout de notes sur Mootse."""
        server = smtplib.SMTP("smtp.ionos.fr", 587)
        server.ehlo()
        server.starttls()
        server.login(sender, password)
        for receiver in receiver_email:
            server.sendmail(sender, receiver, msg.encode('utf-8'))
        server.quit()
        logger.info("succes")
    except:
        logger.critical("echec", exc_info=traceback.format_exc())
        exit(-1)
