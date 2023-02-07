# Mootse
1) Modifier le fichier config.ini avec vos idenfiants.\
2) Modifier la variable path pour correspondre à l'environnement.\
3) Dans le main, run le MootseInit()\
4) Modifier mail.txt (liste des destinataires)\
5) Modifier le main pour avoir afin d'avoir : \
`if __name__ == "__main__":`\
`   path = ""`\
`   MootseRunner(path)`
6) Mettre une crontab sur le main

## Installation sous Windows
* `pip install -r .\requirements.txt`
* `python main.py`
