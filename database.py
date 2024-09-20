import mysql.connector
from mysql.connector import errorcode

# first we need to install mysql-connector-python using `pip install mysql-connector-python`


class DB:
    def __init__(self, db_config: dict):
        self.db_config = db_config

    def __open_connection(self):
        try:
            self.cnx = mysql.connector.connect(**self.db_config)
            print("Connected...")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

    def __close_connection(self):
        if self.cnx.is_connected():
            self.cnx.close()

    def get_databases(self):
        self.__open_connection()
