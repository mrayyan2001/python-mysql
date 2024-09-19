import mysql.connector

# first we need to install mysql-connector-python using `pip install mysql-connector-python`


class DB():
    def __init__(self, db_config: dict):

        self.db_config = db_config
        
    def open_connection(self):
        
        cnx = 
