import os
import json
from google.cloud import datastore
import datetime
import hashlib
from flask import Flask, render_template, request, session, redirect, abort

app = Flask(__name__)
app.secret_key = r"vhfb7qvn84qjmlcifopq0q[0i3"
client = datastore.Client.from_service_account_json(
    "truemission-db-3cc26d81eb59.json")


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
    def __init__(self, id_, title, cost, limit, weight, inner=""):
        self.id = id_
        self.title = title
        self.inner = inner
        self.cost = cost
        self.weight = weight
        self.limit = limit
        self.haveto = self.cost + (7 - self.limit)
        self.client = client

    def commit(self):
        ent = datastore.Entity(client.key("do"))
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
    return render_template("main.html", data_todo=[do("a000120", "国語", 3, 1, 3)])
    """if islogin():
        read = read_do(session["name"], client)
        data = read.listing()
        return render_template("home.html", data=data)
    else:
        return render_template("login.html")"""


@app.route("/logout")
def read():
    if islogin():
        del session["name"]
        return render_template("login.html")
    else:
        return render_template("login.html")


@app.route("/add", methods=["POST"])
def add():
    #必要情報が足りているか
    #idを付与
    
    return


def get():
    data = {"left": [{"title": "abc", "weight": 3, "cost": 2}]}
    return json.dumps(data)
