import smtplib

def alert(matiere):
    sender = ""
    receiver_email = []
    password = ""
    with open("mail.txt", "r") as f:
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
    for receiver in receiver_email : 
        server.sendmail(sender, receiver, msg.encode('utf-8'))
    server.quit()
