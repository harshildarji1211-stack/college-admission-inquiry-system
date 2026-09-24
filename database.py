import mysql.connector


def get_db_connection():
    connection = mysql.connector.connect(
        host="127.0.0.1",
        port=3307,
        user="root",
        password="harshil1211",
        database="college_admission"
    )

    return connection