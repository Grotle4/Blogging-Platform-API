import mysql.connector
import flask
from dotenv import load_dotenv
import os
import json

load_dotenv()

password = os.getenv("PASSWORD")


db = mysql.connector.connect(user='root', password=password, host="localhost", database="bloggingplatformdb")

test_dict = {
    "name" : "this is a test name",
    "title": "this is a test title" #TODO: Consider switching from sending data fully as json to splitting into seperate MySQL Tables
}

test_json = json.dumps(test_dict)

dbcursor = db.cursor()

sql = "INSERT INTO posts (idblog, dataBlog) VALUES (%s, %s)"
val = [(3, test_json)]
dbcursor.executemany(sql, val)

#TODO: Now create way to pull data from SQL table

db.commit()

dbcursor.close()
db.close()