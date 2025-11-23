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


def db_edit(retrieved_item, db_id):
    db = mysql.connector.connect(user='root', password=password, host="localhost", database="bloggingplatformdb")
    dbcursor = db.cursor()

    sql =  "UPDATE posts SET blogTitle = %s, blogContent = %s, blogCategory = %s, blogTags = %s WHERE blogId = %s"
    dbcursor.execute(sql, (retrieved_item["title"], retrieved_item["content"], retrieved_item["category"], retrieved_item["tags"], db_id))

    db.commit()

    dbcursor.close()
    db.close()

@app.route("/posts", methods=['POST'])
def create_blog():
    if request.method == 'POST':
        data = request.get_json()
        db_insert(data)
        print("POST Request")
        return "Post Created", 201



@app.route("/posts/<int:item_id>", methods=['GET', 'PUT', 'DELETE'])
def call_blog(item_id):
    match request.method:
        case 'GET': #TODO: Add seperate route where terms can be looked up to find all articles based on tags
            print("GET Request")
            retrieved_item = db_retrieve(item_id)
            return jsonify(retrieved_item), 200
        case 'PUT':
            print("PUT Request")
            retrieved_item = db_retrieve(item_id)
            data = request.get_json()
            retrieved_item["title"] = data["title"]
            retrieved_item["content"] = data["content"]
            retrieved_item["category"] = data["category"]
            retrieved_item["tags"] = json.dumps(data["tags"])
            db_edit(retrieved_item, item_id)
            return "Blog Post edited successfully", 200
        case 'DELETE': #Add ability to delete an entry from the db based on id
            print("DELETE Request")
            print(item_id)
            return(jsonify(f"DELETED {item_id}"))
#TODO: Add error handing where error code 404 is returned on invalid id or no location found

if __name__ == '__main__':
    app.run()