import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="mysql@742@742",   # change this
        database="college_db"
    )