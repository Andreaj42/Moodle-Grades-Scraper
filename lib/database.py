from logging import getLogger
from traceback import format_exc
from typing import Optional

import mysql.connector

from config.config import DB_HOST, DB_PASSWORD, DB_PORT, DB_USER, PROMO


class DatabaseConnector:

    def __init__(self):
        self.config = {
            'user': DB_USER,
            'password': DB_PASSWORD,
            'host': DB_HOST,
            'port': DB_PORT,
        }
        self.database = PROMO
        self.logger = getLogger()

    def perform_healthcheck(self):
        try:
            cnx = mysql.connector.connect(**self.config)
            cur = cnx.cursor(buffered=True)
            cur.execute("SHOW STATUS LIKE 'Ssl_cipher'")
            cur.close()
            cnx.close()
        except:
            self.logger.critical(
                "Erreur lors de la connexion à MariaDB.", exc_info=format_exc())
            exit(-1)

    def __drop_database(self, name: str):
        sql = f"DROP DATABASE IF EXISTS {name}"
        try:
            cnx = mysql.connector.connect(**self.config)
            cur = cnx.cursor(buffered=True)
            cur.execute(sql)
            cur.close()
            cnx.close()
        except:
            self.logger.critical(
                f"Erreur lors de la suppression de la base {name}.", exc_info=format_exc())
            exit(-1)

    def __create_database(self, name: str):
        sql = f"CREATE DATABASE {name}"
        try:
            cnx = mysql.connector.connect(**self.config)
            cur = cnx.cursor(buffered=True)
            cur.execute(sql)
            cur.close()
            cnx.close()
        except:
            self.logger.critical(
                f"Erreur lors de la création de la base {name}.", exc_info=format_exc())
            exit(-1)

    def __create_table(self, name: str):
        sql = f"""CREATE TABLE Topics (
                Topic VARCHAR(255) NOT NULL,
                Content LONGTEXT,
                Link VARCHAR(255) PRIMARY KEY NOT NULL
            )"""
        try:
            custom_config = self.config
            custom_config["database"] = name
            cnx = mysql.connector.connect(**custom_config)
            cur = cnx.cursor(buffered=True)
            cur.execute(sql)
            cur.close()
            cnx.close()
        except:
            self.logger.critical(
                f"Erreur lors de la création de la table dans la base {name}.", exc_info=format_exc())
            exit(-1)

    def __send_query(self, query: str, val: tuple):
        try:
            # Faire plus jojo
            custom_config = self.config
            custom_config["database"] = self.database

            cnx = mysql.connector.connect(**custom_config)
            cur = cnx.cursor(buffered=True)
            cur.execute(query, val)
            cnx.commit()
            cur.close()
            cnx.close()
        except:
            self.logger.critical(
                f"Erreur lors de l'exécution de la requête : {query}.", exc_info=format_exc())
            exit(-1)

    def __select_query(self, query: str):
        try:
            custom_config = self.config
            custom_config["database"] = self.database
            cnx = mysql.connector.connect(**custom_config)
            cur = cnx.cursor(buffered=True)
            cur.execute(query)
            result = cur.fetchall()
            cur.close()
            cnx.close()
            return result
        except:
            self.logger.critical(
                f"Erreur lors de l'exécution de la requête : {query}.", exc_info=format_exc())
            exit(-1)

    def insert_new_topic(self, topic: str, link: str, content: str):
        sql = f"""INSERT INTO Topics (Topic, Content, Link) VALUES (%s, %s, %s)"""
        val = (topic, content, link)
        self.__send_query(sql, val)

    def update_topic(self, link: str, content: str):
        sql = "UPDATE Topics SET Content = %s WHERE Link = %s"
        val = (content, link)
        self.__send_query(sql, val)

    def setup_database(self):
        self.__drop_database(self.database)
        self.__create_database(self.database)
        self.__create_table(self.database)

    def get_topics(self):
        query = "SELECT * FROM Topics"
        result = self.__select_query(query)
        return result
