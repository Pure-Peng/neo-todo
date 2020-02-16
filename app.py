import os
import json
from google.cloud import datastore
import datetime
import hashlib
from flask import Flask, render_template, request, session, redirect, abort

app = Flask(__name__)
app.secret_key = r"fanvjndipfjijnjv213t5"
jst = datetime.timezone(datetime.timedelta(hours=9), 'JST')
client = datastore.Client.from_service_account_json(
    "todo-dairy-seihou-d40a2b589fc2.json")


def make_id(latest):
    oldchar = latest[0]
    oldnum = int(latest[1:5])
    oldyear = latest[5:]
    if oldnum == 9999:
        char = chr(ord(oldchar) + 1)
    else:
        num = oldnum + 1
    year = str(datetime.datetime.now(jst).year)[2:]
    return char + num + year


def islogin():
    if "name" in session:
        if not client.get(client.key("users", session["name"])) is None:
            return True
        else:
            del session["name"]
            return False
    else:
        return False


class do:
    def __init__(self, id_, title, cost, limit, weight, inner="", client):
        self.id = id_
        self.title = title
        self.inner = inner
        self.cost = cost
        self.weight = weight
        self.limit = limit
        self.haveto = self.cost + (7 - self.limit)
        self.client = client

    def commit(self):
        ent = datastore.Entity(client.key("diary"))
        ent["id"] = self.id
        ent["title"] = self.title
        ent["inner"] = self.inner  # memoの場合
        ent["cost"] = self.cost  # かかる労力(4が標準)
        ent["limit"] = self.limit  # 提出までの残り日数
        ent["weight"] = self.weight  # その行動に必要な時間の量(4が標準)
        ent["haveto"] = self.haveto  # 緊急性
        self.client.put(ent)


@app.route("/")
def read():
    return render_template("main.html")
    """if islogin():
        read = read_do(session["name"], client)
        data = read.listing()
        return render_template("home.html", data=data)
    else:
        return render_template("login.html")"""


@app.route("/add", methods=["POST"])
def add():
    # 必要情報が足りているか
    try:
        if request.form["title"] == "":
            return show_error("TITLE HASN'T WRITTEN.")
        elif request.form["cost"] == "":
            return show_error("COST HASN'T WRITTEN.")
        elif request.form["limit"] == "":
            return show_error("LIMIT HASN'T WRITTEN.")
        elif request.form["weight"] == "":
            return show_error("WEIGHT HASN'T WRITTEN.")
    except:
        return show_error("THINGS HAS AN ERROR.")
    # idを付与

    return


@app.route("/get", methods=["POST"])
def get():
    data = {"left": [{"title": "abc", "weight": 3, "cost": 2}],
            "right": [{"title":}]}
    return json.dumps(data)
