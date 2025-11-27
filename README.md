# Blogging Platform API

A lightweight RESTful API built with **Flask** and **MySQL**, designed to manage blog posts with full Create, Read, Update, and Delete (CRUD) functionality. The API supports tag-based searching, input validation, and returns structured JSON responses for easy integration with frontend applications.

---

## Table of Contents
1. Introduction  
2. Features  
3. Tech Stack  
4. Installation  
5. Environment Variables  
6. Database Setup  
7. Running the Server  
8. API Endpoints  
9. Example JSON Bodies  
10. Troubleshooting  

---

## Introduction

The **Blogging Platform API** provides a simple backend service that allows a client application to store, retrieve, update, and delete blog posts. Posts include fields such as `title`, `content`, `category`, and a list of `tags`, which are stored as JSON in the database. The API includes validation for request formatting and data types, tag searching, and structured JSON responses for retrieving single or multiple posts.

---

## Features

- ✔ Full CRUD operations  
- ✔ Tag-based search  
- ✔ Input validation  
- ✔ Automatic timestamp formatting  
- ✔ JSON-based tag storage using MySQL JSON fields  
- ✔ Clean response formatting  

---

## Tech Stack

- **Python 3.x**  
- **Flask**  
- **MySQL**  
- **mysql-connector-python**  
- **python-dotenv**  

---

## Installation

### **1. Clone the Repository**
```bash
git clone https://github.com/Grotle4/Blogging-Platform-API.git
cd <your-project-folder>
```

### **2. Install Required Python Packages**
(Optional but recommended — create a virtual environment)

```bash
python -m venv venv
source venv/bin/activate     # Linux / macOS
venv\Scripts\activate      # Windows
```

Install dependencies:

```bash
pip install flask mysql-connector-python python-dotenv
```

---

## Environment Variables

Create a `.env` file in your project root:

```
PASSWORD=your_mysql_password
```

This is used by the API to authenticate with MySQL.

---

## Database Setup

### **1. Create the MySQL Database**

```sql
CREATE DATABASE bloggingplatformdb;
USE bloggingplatformdb;
```

### **2. Create the Required Table**

```sql
CREATE TABLE posts (
    blogId INT AUTO_INCREMENT PRIMARY KEY,
    blogTitle VARCHAR(255) NOT NULL,
    blogContent TEXT NOT NULL,
    blogCategory VARCHAR(255) NOT NULL,
    blogTags JSON NOT NULL,
    timeCreated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    timeUpdated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

---

## Running the Server

Start the Flask application:

```bash
python REST_api.py
```

Default server location:

```
http://127.0.0.1:5000
```

---

## API Endpoints

### 📌 **POST /posts**
Create a new blog post.  
Validates required keys and types.

Returns:
- `201 Created`
- `400 Bad Request` on validation errors

---

### 📌 **GET /posts**
Retrieve all posts.  
Supports tag search:

```
GET /posts?tags=python
```

---

### 📌 **GET /posts/<id>**
Retrieve a specific post.

Responses:
- `200 OK`
- `404 Not Found`

---

### 📌 **PUT /posts/<id>**
Update a blog post.  
Validates fields.

Responses:
- `200 OK`
- `400 Bad Request`

---

### 📌 **DELETE /posts/<id>**
Deletes a post.

Responses:
- `204 No Content`
- `404 Not Found`

---

## Example JSON Bodies

### ✔ POST / PUT Request Example
```json
{
  "title": "How to Build an API",
  "content": "This is a guide on building APIs using Flask.",
  "category": "Programming",
  "tags": ["flask", "api", "tutorial"]
}
```

### ✔ GET Response Example
```json
{
  "id": 3,
  "title": "How to Build an API",
  "content": "This is a guide on building APIs using Flask.",
  "category": "Programming",
  "tags": ["flask", "api", "tutorial"],
  "timeCreated": "2025-01-07 10:15:30.000000",
  "timeUpdated": "2025-01-07 10:15:30.000000"
}
```

---

## Troubleshooting

### MySQL connection issues
- Ensure MySQL server is running  
- Verify `.env` file contains correct password  
- Confirm database name: `bloggingplatformdb`

### Validation issues
Required keys:
- `title`
- `content`
- `category`
- `tags`

Correct types:
- Strings for title, content, category  
- List for tags  

### Tag search not returning results
Tag match must be exact:

```
GET /posts?tags=python
```

---

### Inspiration

---
https://roadmap.sh/projects/blogging-platform-api

