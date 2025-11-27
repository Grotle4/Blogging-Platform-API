import mysql.connector
from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
import json

load_dotenv()

password = os.getenv("PASSWORD")

app = Flask(__name__)
app.json.sort_keys = False


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
        "tags": json.loads(result[4]),
        "timeCreated": result[5].strftime("%Y-%m-%d %H:%M:%S.%f"),
        "timeUpdated": result[6].strftime("%Y-%m-%d %H:%M:%S.%f")
    }
    print(retrieved_dict)

    dbcursor.close()
    db.close()
    return retrieved_dict


def db_retrieve_all():
    db = mysql.connector.connect(user='root', password=password, host="localhost", database="bloggingplatformdb")
    dbcursor = db.cursor()

    sql =  "SELECT * FROM posts"
    dbcursor.execute(sql)

    results = dbcursor.fetchall()

    dbcursor.close()
    db.close()
    return results

def db_edit(retrieved_item, db_id):
    db = mysql.connector.connect(user='root', password=password, host="localhost", database="bloggingplatformdb")
    dbcursor = db.cursor()

    sql =  "UPDATE posts SET blogTitle = %s, blogContent = %s, blogCategory = %s, blogTags = %s WHERE blogId = %s"
    dbcursor.execute(sql, (retrieved_item["title"], retrieved_item["content"], retrieved_item["category"], retrieved_item["tags"], db_id))

    db.commit()

    dbcursor.close()
    db.close()


def db_delete(db_id):
    db = mysql.connector.connect(user='root', password=password, host="localhost", database="bloggingplatformdb")
    dbcursor = db.cursor()

    sql = "DELETE FROM posts WHERE blogId = %s"
    dbcursor.execute(sql, (db_id,))

    db.commit()

    dbcursor.close()
    db.close()

def db_exists(db_id):
    db = mysql.connector.connect(user='root', password=password, host="localhost", database="bloggingplatformdb")
    dbcursor = db.cursor()

    sql = "SELECT EXISTS(SELECT 1 FROM posts WHERE blogId = %s)"
    dbcursor.execute(sql, (db_id,))

    entry_exists = dbcursor.fetchone()[0]

    dbcursor.close()
    db.close()

    if entry_exists:
        return True
    else:
        return False


def validate_dict_formatting(data):
    required_keys = {"title", "content", "category", "tags"}
    keys_list = list(required_keys)
    found_keys = set(data.keys())
    print(f"found: {found_keys}")
    unneeded_keys = found_keys - required_keys
    errors = []
    
    for idx in range(len(keys_list)):
        if keys_list[idx] not in data:
            error = f"Error: required key: '{keys_list[idx]}' not found in request, please add proper key and try again"
            errors.append(error)

    if unneeded_keys:
        error = f"Error: invalid keys found. {unneeded_keys} are not valid keys, remove them and try again."
        errors.append(error)
    
    return errors

def validate_dict_types(data):
    types = [str, str, str, list]
    keys = ["title", "content", "category", "tags"]
    errors = []

    for idx in range(len(keys)):
        if isinstance(data[keys[idx]], types[idx]):
            print(f"Proper type match, key '{keys[idx]}' is correctly a {types[idx]}")
        else:
            error = (f"Incorrect type match, key '{keys[idx]}' should be type: {types[idx]}")
            errors.append(error)
    return errors
    

def db_tag_search(tags):
    db = mysql.connector.connect(user='root', password=password, host="localhost", database="bloggingplatformdb")
    dbcursor = db.cursor()
    json_value = json.dumps([tags])

    print(f"this is the str: {json_value}")
    sql = "SELECT * FROM posts WHERE JSON_CONTAINS(blogTags, %s)"
    dbcursor.execute(sql, (json_value,))

    results = dbcursor.fetchall()
    print(results)
    return results


def create_get_dict(results):
    result_list = []
    for result in tuple(results):
        print(f"result: {result}")
        print(type(result))
        results_dict = {
            "id": result[0],
            "title": result[1],
            "content": result[2],
            "category": result[3],
            "tags": json.loads(result[4]),
            "timeCreated": result[5].strftime("%Y-%m-%d %H:%M:%S.%f"),
            "timeUpdated": result[6].strftime("%Y-%m-%d %H:%M:%S.%f")
            }
        result_list.append(results_dict)
    return result_list

@app.route("/posts", methods=['POST', 'GET'])
def blog():
    if request.method == 'POST':
        data = request.get_json()
        format_errors = validate_dict_formatting(data)
        if not format_errors:
            type_errors = validate_dict_types(data)
            if not type_errors:
                db_insert(data)
                print("POST Request")
                return "Post Created", 201
            else:
                return type_errors, 400
        else:
            return format_errors, 400
                    
    if request.method == 'GET':
        if not request.args:
            print("no argument given")
            results = db_retrieve_all()
            result_list = create_get_dict(results)
            return jsonify(result_list)
        else:
            tags = request.args.get("tags")
            tagged_results = db_tag_search(tags)
            result_list = create_get_dict(tagged_results)
            return jsonify(result_list)
    



@app.route("/posts/<int:item_id>", methods=['GET', 'PUT', 'DELETE'])
def call_blog(item_id):
    entry_exists = db_exists(item_id)
    if entry_exists:
        match request.method:
            case 'GET':
                print("GET Request")
                retrieved_item = db_retrieve(item_id)
                return jsonify(retrieved_item), 200
            case 'PUT':
                print("PUT Request")
                retrieved_item = db_retrieve(item_id)
                data = request.get_json()
                format_errors = validate_dict_formatting(data)
                if not format_errors:
                    type_errors = validate_dict_types(data)
                    if not type_errors:
                        retrieved_item["title"] = data["title"]
                        retrieved_item["content"] = data["content"]
                        retrieved_item["category"] = data["category"]
                        retrieved_item["tags"] = json.dumps(data["tags"])
                        db_edit(retrieved_item, item_id)
                        return "Blog Post edited successfully", 200
                    else:
                        return type_errors, 400
                else:
                    return format_errors, 400
            case 'DELETE':
                print("DELETE Request")
                db_delete(item_id)
                return "", 204
    else:
        return "Item not found", 404



if __name__ == '__main__':
    app.run()