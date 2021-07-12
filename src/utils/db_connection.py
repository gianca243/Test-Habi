"""
Database SQL connection
"""
import os
import mysql.connector

def db_connection():
  db_host = os.environ['SQL_HOST']
  db_user = os.environ['SQL_USER']
  db_password = os.environ['SQL_PASSWORD']
  db_port = os.environ['SQL_PORT']
  db_database = os.environ['SQL_DATABASE']
  mydb = mysql.connector.connect(
    host = db_host,
    port = db_port,
    user = db_user,
    password = db_password,
    database = db_database
  )
  
  return mydb