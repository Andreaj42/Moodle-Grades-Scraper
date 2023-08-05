import sys

import mysql.connector

from config.config import DB_HOST, DB_PASSWORD, DB_PORT, DB_USER

try:
    cnx = mysql.connector.connect(
        user = DB_USER,
        password = DB_PASSWORD,
        host = DB_HOST,
        port = DB_PORT
    )
    cnx.close()
    sys.exit(0)
except:
    sys.exit(1)