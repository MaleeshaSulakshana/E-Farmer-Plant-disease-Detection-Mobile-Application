import mysql.connector


def connector():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="efarmer"
    )

    return conn
