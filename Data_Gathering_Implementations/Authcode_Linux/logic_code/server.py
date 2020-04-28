import time

from flask import Flask, request
from flask_restful import Resource, Api
from gevent.pywsgi import WSGIServer
import os
import platform

bar=''
if platform.system() == "Linux":
    bar="/"
elif platform.system() == "Windows":
    bar='\\'

app = Flask(__name__)
api = Api(app)
pc_directory = str(os.getcwd()) + bar + "pc"
users_directory = str(os.getcwd()) + bar + "users"
error_directory=str(os.getcwd()) + bar + "errors"
window_pc=60

class pc(Resource):

    def post(self, userid):
        vector = request.data.decode("utf-8")
        vector = vector[:-1]
        vector = vector +","+userid+"\n"
        file_path = pc_directory + bar + userid
        if os.path.exists(file_path):
            append_write = 'a'  # append if already exists
        else:
            append_write = 'w'  # make a new file if not
        file = open(file_path, append_write)
        file.write(vector)
        file.close()

        return window_pc

# User login and register class
# GET for login
# POST for register
class users(Resource):
    def get(self):
        try:
            info = request.data.decode("utf-8")
            credentials = info.split(':')
            id = credentials[0]
            passwd = credentials[1]
            file_path = users_directory + bar + id

            if not os.path.exists(file_path):
                return 400

            file = open(file_path, 'r')
            passwd_stored = file.read()
            file.close()

            if passwd_stored != passwd:
                return 300

            return 200
        except:
            return 400

    def post(self):
        try:
            info = request.data.decode("utf-8")
            credentials = info.split(':')
            id = credentials[0]
            passwd = credentials[1]
            file_path = users_directory + bar + id
            if os.path.exists(file_path):
                return 400
            file = open(file_path, 'w')
            file.write(passwd)
            file.close()
            return 200
        except:
            return 400


class errors(Resource):
    def post(self):
        try:
            info = request.data.decode("utf-8")
            error_path=error_directory+bar+"errors"
            file=open(error_path,'a')
            file.write(info)
            file.close()
        except:
            pass
    
def launch_REST_Server():
    if not os.path.exists(pc_directory):
        os.makedirs(pc_directory)
    if not os.path.exists(users_directory):
        os.makedirs(users_directory)
    if not os.path.exists(error_directory):
        os.makedirs(error_directory)
    api.add_resource(pc, '/pc/<userid>')  # Route_1
    api.add_resource(users, '/user')
    api.add_resource(errors,'/errors')
    http_server = WSGIServer(('0.0.0.0', 5002), app)
    http_server.serve_forever()


if __name__ == "__main__":
    launch_REST_Server()
