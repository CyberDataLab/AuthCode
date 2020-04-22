import time
from winreg import SetValueEx, OpenKey, HKEY_CURRENT_USER, KEY_ALL_ACCESS, REG_SZ, CloseKey
import os
import hashlib

from win32con import SW_SHOW

from logic_code import extract_features, logger
import requests
from pathlib import Path
import sys

urlServer = extract_features.urlServer

#Create work directory

home = Path.home()
path = str(home) + "\\Authcode"
path_idUser = path + "\\" + "idUser"


def generate_hash_passwd(passwd):
    hash_object = hashlib.sha1(passwd.encode("UTF-8"))
    hex_dig = hash_object.hexdigest()
    return hex_dig


# Register user
def registrer(user, passwd):
    try:
        response = requests.post(urlServer + "/user", data=str(user + ':' + passwd).encode("utf-8"))
        response = int(response.text)
        if response == 200:
            print("User correctly registered")
            file = open(path_idUser, 'w')
            file.write(user + ':' + passwd)
            file.close()
            return 200
        elif response == 400:
            print("Username not available")
            return 400
    except:
        return 500


# Do login
def login():
    try:
        if os.path.exists(path_idUser):
            try:
                fichId = open(path_idUser, "r")
                partesCredenciales = fichId.read().split(':')
                user = partesCredenciales[0]
                passwd = partesCredenciales[1]
                fichId.close()
                response = requests.get(urlServer + "/user", data=str(user + ':' + passwd).encode("utf-8"))
                response = int(response.text)
                if response != 200:
                    print("Login could not be done using stored credentials.")
                    os.remove(path_idUser)
                else:
                    print("Successful login.")
                    return 200
            except:
                print("Unable to reach the server.")
                return 500

        option = 0
        while option == 0:
            while not (option == 1 or option == 2):
                entrada = input("Do you want to login (1) or register (2)? ")
                if entrada == "1" or entrada == "2":
                    option = int(entrada)
            user=""
            passwd=""

            try:
                user = input("Username: ")
                passwd = input("Password: ")
                passwd = generate_hash_passwd(passwd)
            except Exception as e:
                print(str(e))

            response = 0
            if option == 1:
                try:
                    response = requests.get(urlServer + "/user", data=str(user + ':' + passwd).encode("utf-8"))
                    response = int(response.text)
                    if response != 200:
                        option = 0
                        print("Incorrect username or password.")
                    else:
                        file = open(path_idUser, 'w')
                        file.write(user + ':' + passwd)
                        file.close()
                        print("Successful login.")
                        return 200
                except:
                    print("Unable to reach the server.")
                    return 500

            elif option == 2:
                response = registrer(user, passwd)
                if response == 400:
                    option = 0
                    print("Username not available, try a new one or do login.")
                elif response == 200:
                    response = requests.get(urlServer + "/user", data=str(user + ':' + passwd).encode("utf-8"))
                    response = int(response.text)
                    if response == 200:
                        print("Successful login.")
                        return 200
                elif response == 500:
                    print("Unable to reach the server.")
                    return 500
    except Exception as e:
        print(str(e))
        return 500


# Add .py scriot to the app registry, so the app is launched at windows start
def addStartup():
    new_file_path = str(os.getcwd()) + "\\logger.exe"
    keyVal = r'Software\Microsoft\Windows\CurrentVersion\Run'
    key2change = OpenKey(HKEY_CURRENT_USER, keyVal, 0, KEY_ALL_ACCESS)
    SetValueEx(key2change, 'Authcode', 0, REG_SZ, new_file_path)
    CloseKey(key2change)


# Hide terminal
def hide():
    import win32console
    import win32gui
    win = win32console.GetConsoleWindow()
    win32gui.ShowWindow(win, 0)

# Show terminal
def show():
    import win32console
    import win32gui
    win = win32console.GetConsoleWindow()
    win32gui.ShowWindow(win, SW_SHOW)

if __name__ == '__main__':
    if len(sys.argv)==2 and sys.argv[1]=="install":
        addStartup()
        if os.path.exists(path):
            if os.path.exists(path_idUser):
                os.remove(path_idUser)
            if os.path.exists(path+"\\ventana"):
                os.remove(path+"\\ventana")

    connected = 0
    loginRes = login()
    if loginRes == 200:
        print("Data collection service launched successfully.")
        connected = 1

    print("This window will be closed in two seconds.")
    time.sleep(2)
    hide()
    if not os.path.exists(path_idUser):
        while connected==0:
            time.sleep(300)
            show()
            loginRes = login()
            if loginRes == 200:
                print("Data collection service launched successfully.")
                connected = 1
            time.sleep(2)
            hide()

    while(True):
        try:
            logger.launch()
        except Exception as e:

            # Create working directory
            home = Path.home()
            path_logs = str(home) + "\\Authcode"
            if not os.path.exists(path_logs):
                os.mkdir(path_logs)

            # Create mouse and keyboard, and apps log temporal files
            path = path_logs + "\\mouse_keyboard_log_service.txt"
            if os.path.exists(path):
                try:
                    os.remove(path)
                except:
                    pass

            path_apps = path_logs + "\\apps_log_service.txt"
            if os.path.exists(path_apps):
                try:
                    os.remove(path_apps)
                except:
                    pass
            path_ventana = path_logs + "\\ventana"
            if os.path.exists(path_ventana):
                try:
                    os.remove(path_ventana)
                except:
                    pass
            text=str(e)+"\n"
            print(text)
            requests.post(urlServer + "/errors", data=text.encode("utf-8"))