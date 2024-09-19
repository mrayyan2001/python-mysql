import streamlit as st
import mysql.connector
from database import DB

# first you need to install mysql connector for python uinsg `pip3 install mysql-connector-python`

# define the database config
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "root",
}


db = DB(db_config)

st.write(db.cnx)
st.write(db.cursor)
