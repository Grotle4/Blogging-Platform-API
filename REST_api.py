import mysql.connector
import flask
from dotenv import load_dotenv
import os
import json
import datetime

load_dotenv()

password = os.getenv("PASSWORD")


db = mysql.connector.connect(user='root', password=password, host="localhost", database="bloggingplatformdb")



test_dict = {
    "title" : "this is a test name",
    "content": "this is a test title",
    "category": "this is the category",
    "tags": ["tag 1", "tag 2"]
}



def db_insert(test_dict, db):

    dbcursor = db.cursor()

    sql = "INSERT INTO posts (blogTitle, blogContent, blogCategory, blogTags) VALUES (%s, %s, %s, %s)"
    dbcursor.execute(sql, (test_dict["title"], test_dict["content"], test_dict["category"], json.dumps(test_dict["tags"])))

    db.commit()
    dbcursor.close()
    db.close()

def db_retrieve(db_id, db):
    dbcursor = db.cursor()

    sql =  "SELECT * FROM posts WHERE blogId = %s"
    dbcursor.execute(sql, (db_id,))
    result = dbcursor.fetchone()
    retrieved_dict = {
        "id": result[0],
        "title": result[1],
        "content": result[2],
        "category": result[3],
        "tags": result[4],
        "timeCreated": result[5].strftime("%Y-%m-%d %H:%M:%S.%f"),
        "timeUpdated": result[6].strftime("%Y-%m-%d %H:%M:%S.%f")
    }
    print(retrieved_dict)

    dbcursor.close()
    db.close()

db_retrieve(3, db)
#db_insert(test_dict, db)
