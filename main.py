import streamlit as st
import mysql.connector
from mysql.connector import errorcode
from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate
import os

print(os.environ["GOOGLE_API_KEY"])
llm = GoogleGenerativeAI(model="gemini-1.5-flash")

template = """
Based on the given info about the MySQL databases:
{databases_info}

Give me the MySQL query to do this user request:
{user_request}

if the request can be from different database give answer for each one.
"""

prompt_template = PromptTemplate(template=template, input_variables=["databases_info", "user_request"])

if "is_connected" not in st.session_state:
    st.session_state.is_connected = False
with st.form("config-form"):
    host = st.text_input("Host")
    user = st.text_input("User")
    password = st.text_input("Password", type="password")

    if st.form_submit_button("Connect"):
        if host and user and password:
            st.session_state.db_config = {
                "host": host,
                "user": user,
                "password": password,
                "buffered": True,
            }
            try:
                st.session_state.cnx = mysql.connector.connect(**st.session_state.db_config)
                if st.session_state.cnx.is_connected():
                    st.success(f"Connected into {st.session_state.db_config["user"]}@{st.session_state.db_config["host"]}")
                    st.session_state.is_connected = True
            except mysql.connector.Error as err:
                st.warning(err)
                st.session_state.is_connected = False
                
        else:
            st.warning("All filed are required.")

if st.session_state.is_connected:
    with st.session_state.cnx.cursor() as cursor:
        databases_info = {}
        result1 = cursor.execute("SHOW DATABASES WHERE `database` NOT IN ('mysql', 'performance_schema', 'information_schema', 'sys');")
        databases = cursor.fetchall()
        databases = [database[0] for database in databases]

        for database in databases:
            result2 = cursor.execute(F"SHOW FULL TABLES FROM {database} WHERE Table_type != 'VIEW'")
            tables = cursor.fetchall()
            tables = [table[0] for table in tables]
            
            databases_info[database] = {}
            for table in tables:
                result3 = cursor.execute(F"SHOW CREATE TABLE {database}.{table}")
                columns = cursor.fetchall()
                columns = [column[1] for column in columns]
                databases_info[database][table] = columns

    user_request = st.text_input("User Request")
    
    if st.button("Get Query"):
        if not user_request:
            st.warning("What's you request?")
        else:
            prompt = prompt_template.format(databases_info=databases_info, user_request=user_request)

            llm_result = llm.invoke(prompt)
            st.write(llm_result)
        
    
