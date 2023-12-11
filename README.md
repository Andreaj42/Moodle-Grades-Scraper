
# Moodle Grades Scraper
> :warning: **This project is now maintained by L'Usine Logicielle: https://github.com/L-Usine-Logicielle/Moodle-Grades-Scraper**

Moodle Grades Scraper is a simple tool to be notified of new grades on Moodle 💯.

## Features 
- E-mail alerting 📫
- Discord notifications (webhook) 🎤
- MariaDB storage 💾
- Running with Docker and Docker Compose 🐳
- Written in Python 3 🐍

## Installation 📓
Before using this project, ensure that the following requirements are met:
- Docker and Docker Compose need to be installed
- Even though we do not recommend Moodle Grades Scraper users to run the application from source, you may need to run from source for testing purposes or to enjoy the latest feature that is not released yet. To do so, make sure ✔️ :
  - Python 3 (tested with v3.9.12) is installed on your system
  - MariaDB (tested with v10.4) is installed on your system

### Docker 🐳
To install Moodle Grades Scraper with Docker and Docker Compose, follow these steps:

1. Clone the project
```
git clone https://github.com/Andreaj42/Moodle-Grades-Scraper.git
```
2. Go to the project's directory
```
cd Moodle-Grades-Scraper
```
3. Fill the .env file
```
vi .env
```
4. Run the docker-compose.yaml
```
docker compose up -d
```

### From source 🗝️
To install Moodle Grades Scraper from source, follow these steps:

1. Clone the project
```
git clone https://github.com/Andreaj42/Moodle-Grades-Scraper.git
```
2. Go to the project's directory
```
cd Moodle-Grades-Scraper
```
3. Create a Python virtual environment
```
python -m venv _venv
```
4. Activate the virtual environment
```
source _venv/bin/activate
```
5. Set the variables of the .env file in your system
```
export VARIABLE_NAME=VALUE
```
6. Install the dependencies with pip 
```
pip install -e .
```
7. Start the application
```
python main.py
```

### About the .env 🔍

| Variable          | Description               
|---------------------|------------------------------------------|
| MOOTSE_URL     | Moodle URL (i.e: https://my-moodle.org/)    |
| MOOTSE_USERNAME     | Moodle username                          |    
| MOOTSE_PASSWORD     | Moodle password                                 |    
| MAIL_USERNAME       | SMTP username                     |    
| MAIL_PASSWORD       | SMTP password |    
| MAIL_SERVER         | SMTP server                            |    
| MAIL_PORT           | SMTP port                                      |    
| MAIL_RECIPIENTS     | **Optional** - Mail recipients separated by ';' (i.e: "user1@mail.org;user2@mail.org").                       |    
| DISCORD_WEBHOOK_URL | **Optional** - Discord webhook URL.                                        |    
| DB_HOST             | MariaDB host                          |    
| DB_USER             | MariaDB user                                     |    
| DB_PASSWORD         | MariaDB password                                   |    
| DB_PORT             | MariaDB port                                     |    
| PROMO               | The name of your promotion, in a single word (i.e: myWonderfulPromo)                                      |    
| MYSQL_ROOT_PASSWORD | **Optional in source mode** - MariaDB password when running with Docker Compose                                   |    
| SCAN_INTERVAL       | Scan interval in seconds (i.e: 120 for 2 minutes)                                      |    

## Report a bug 🐛
Simply open an issue in this repository.


## Disclaimer ⚠️
Moodle Grades Scraper is not part of Moodle.
