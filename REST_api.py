import mysql.connector
from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
import json
import datetime

load_dotenv()

password = os.getenv("PASSWORD")

app = Flask(__name__)


test_dict = {
    "title" : "this is a test name",
    "content": "this is test content",
    "category": "this is the category",
    "tags": ["tag 1", "tag 2"]
}

def db_insert(post_dict):
    db = mysql.connector.connect(user='root', password=password, host="localhost", database="bloggingplatformdb")
    dbcursor = db.cursor()

    sql = "INSERT INTO posts (blogTitle, blogContent, blogCategory, blogTags) VALUES (%s, %s, %s, %s)"
    dbcursor.execute(sql, (post_dict["title"], post_dict["content"], post_dict["category"], json.dumps(post_dict["tags"])))

    db.commit()
    dbcursor.close()
    db.close()

def db_retrieve(db_id):
    db = mysql.connector.connect(user='root', password=password, host="localhost", database="bloggingplatformdb")
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
    return retrieved_dict


@app.route("/posts", methods=['POST'])
def create_blog():
    if request.method == 'POST':
        data = request.get_json()
        db_insert(data)
        print("POST Request")
        return jsonify("POSTED")



@app.route("/posts/<int:item_id>", methods=['GET', 'PUT', 'DELETE'])
def call_blog(item_id):
    match request.method:
        case 'GET':
            print("GET Request")
            retrieved_item = db_retrieve(item_id)
            return(jsonify(f"GETTED item #{item_id}: {retrieved_item}"))
        case 'PUT': #TODO: Add ability to retrieve from db and then edit existing data, returning it to db with update time changed
            print("PUT Request")
            print(item_id)
            return(jsonify(f"PUTTED {item_id}"))
        case 'DELETE': #Add ability to delete an entry from the db based on id
            print("DELETE Request")
            print(item_id)
            return(jsonify(f"DELETED {item_id}"))


if __name__ == '__main__':
    app.run()