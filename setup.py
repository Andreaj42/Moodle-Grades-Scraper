from setuptools import setup

setup(
    name='mootse-runner',
    version='1.1',
    install_requires=[
        'APScheduler==3.10.1',
        'beautifulsoup4==4.12.2',
        'bs4==0.0.1',
        'certifi==2022.12.7',
        'charset-normalizer==3.1.0',
        'idna==3.4',
        'requests==2.28.2',
        'mysql-connector-python==8.0.33',
        'setuptools==58.1.0',
        'soupsieve==2.4',
        'urllib3==1.26.15'
    ],
    description='Système de notifications pour Mootse, le Moodle de Télécom Saint-Etienne',
)
