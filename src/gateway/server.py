import os
import gridfs
import pika
import json
from flask import Flask, request
from flask_pymongo import PyMongo
from auth import validate
from auth_svc import access

server = Flask(__name__)
server.config["MONGO_URI"] = "mongodb://host.minikube.internal:27017/videos"

mongo = PyMongo(server)

db_name = mongo.db
fs = gridfs.GridFS(db_name)

# configuring rabbitmq connection
connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
channel = connection.channel()

@server.route('/login', methods=['POST'])
def login():
    token, err = access.login(request)

    if not err:
        return token
    
    return err