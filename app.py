from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from db import open, close, create_table, all_lists, get_items
import db
import json

app = Flask(__name__)

conn, cur = open()
cur.execute("CREATE TABLE IF NOT EXISTS lists (id INTEGER PRIMARY KEY, list_name TEXT NOT NULL)")
close(conn, cur)


@app.route("/", methods = ["GET", "POST"])
def index():
    return render_template("index.html", lists = all_lists())

@app.route("/newlist", methods = ["GET","POST"])
def new_list():
    list_name = request.form.get("name")
    if list_name:
        name = create_table(list_name)
        items = get_items(list_name)
        return render_template("list.html", listname = list_name, list = items)
    else:
        redirect("/")
        return index()

@app.route("/editlist/<list_name>", methods=["GET","POST"])
def edit_list(list_name):
    item = request.form.get("item")
    if item:
        db.insert_item(list_name, item)
    items = get_items(list_name)
    return render_template("list.html", listname = list_name, list = items)

@app.route("/deletelists", methods = ["POST", "GET"])
def delete_lists():
    trash = request.get_json() #list of id's
    db.delete_lists(trash) 
    return render_template("index.html", lists = all_lists())

@app.route("/deleteitems", methods=["GET", "POST"])
def delete_items():
    trash = request.get_json()
    list_name = trash.pop()
    items = db.delete_items(list_name, trash) 
    return render_template("list.html", listname = list_name, list = items)

if __name__ == '__main__':
    app.run(debug=True)