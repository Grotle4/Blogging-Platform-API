import mysql.connector
import flask
from dotenv import load_dotenv
import os
import json

load_dotenv()

password = os.getenv("PASSWORD")


db = mysql.connector.connect(user='root', password=password, host="localhost", database="bloggingplatformdb")



test_dict = {
    "id": 2,
    "title" : "this is a test name",
    "content": "this is a test title",
    "category": "this is the category",
    "tags": ["tag 1", "tag 2"]
}

test_json = json.dumps(test_dict)

dbcursor = db.cursor()

sql = "INSERT INTO posts (blogId, blogTitle, blogContent, blogCategory, blogTags) VALUES (%s, %s, %s, %s, %s)"
dbcursor.execute(sql, (test_dict["id"],test_dict["title"], test_dict["content"], test_dict["category"], json.dumps(test_dict["tags"])))

#TODO: Now create way to pull data from SQL table

db.commit()

dbcursor.close()
db.close()