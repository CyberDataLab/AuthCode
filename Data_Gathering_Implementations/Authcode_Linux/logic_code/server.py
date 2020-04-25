import time

from flask import Flask, request
from flask_restful import Resource, Api
from gevent.pywsgi import WSGIServer
import os
import platform

spacebar=''
if platform.system() == "Linux":
    spacebar="/"
elif platform.system() == "Windows":
    spacebar='\\'

app = Flask(__name__)
api = Api(app)
android_directory = str(os.getcwd()) + spacebar+"android"
pc_directory = str(os.getcwd()) + spacebar + "pc"
users_directory = str(os.getcwd()) + spacebar + "users"
error_directory=str(os.getcwd()) + spacebar + "errors"
window_pc=60
window_android=60

class pc(Resource):

    def post(self, userid):
        vector = request.data.decode("utf-8")
        path_file = pc_directory + spacebar + userid
        if os.path.exists(path_file):
            append_write = 'a'  # append if already exists
        else:
            append_write = 'w'  # make a new file if not
        file = open(path_file, append_write)
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
            path_fichero = users_directory + spacebar + id

            if not os.path.exists(path_fichero):
                return 400

            file = open(path_fichero, 'r')
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
            path_fichero = users_directory + spacebar + id
            if os.path.exists(path_fichero):
                return 400
            file = open(path_fichero, 'w')
            file.write(passwd)
            file.close()
            return 200
        except:
            return 400


class errors(Resource):
    def post(self):
        try:
            info = request.data.decode("utf-8")
            error_path=error_directory+spacebar+"errors"
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
