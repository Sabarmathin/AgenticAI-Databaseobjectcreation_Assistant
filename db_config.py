import mysql.connector


def connect_db():
    connection = mysql.connector.connect(
        host="localhost",
        port="3306",
        user="root",
        password="",
        database="agent_db"
    )

    return connection