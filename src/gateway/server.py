import os
import gridfs
import pika
import json
from flask import Flask, request
from flask_pymongo import PyMongo
from auth import validate
from auth_svc import access
from storage import utils

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

@server.route('/upload', methods=["POST"])
def upload():
    access, err = validate.token(request)

    access = json.loads(access)

    if access['is_admin']:
        if len(request.files) != 1:
            return "Only 1 file can be uploaded!!", 400
        
        for filename, file in request.files.items():
            error_response = utils.upload_file_in_mongodb(file, fs, channel, access)

            if error_response:
                return error_response
            
        return "Success!", 200
    
    return "Not Athorized!!", 401