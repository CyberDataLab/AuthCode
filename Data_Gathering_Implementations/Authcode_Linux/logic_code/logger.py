# coding=utf-8

import time
import psutil
import os
from pynput import mouse
import threading
import subprocess as sp
from logic_code import extract_features
from pathlib import Path
from logic_code.keyboard import *
import notify2
import sys

# Lamba to obtain milisecond timestamp
current_time = lambda: int(time.time() * 1000)

# Generate work directory
home = Path.home()
path_logs = str(home) + "/Authcode"
if not os.path.exists(path_logs):
    os.mkdir(path_logs)

# Generate temporal log files
path = path_logs + "/mouse_keyboard_log_service.txt"
if os.path.exists(path):
    os.remove(path)
path_apps= path_logs + "/apps_log_service.txt"
if os.path.exists(path_apps):
    os.remove(path_apps)
file_logs = open(path, 'a')

pids = []


#Read PIDs of the processes with active windows (applications)
def read_window_pids():
    global pids
    f = os.popen("wmctrl -l")
    lines=f.read().split("\n")
    windows = []
    for line in lines:
        line = line.replace("  ", " ")
        win = tuple(line.split(" ", 3))
        windows.append(win)
    for win in windows:
        if(win[0]!=''):
            f = os.popen("xprop -id "+win[0]+" _NET_WM_PID")
            lines = f.read().split("\n")
            pid_split=lines[0].split(" ")
            pid=int(pid_split[2])
            pids.append(pid)
    return True


#Obtain process pids using app name
def find_pids_by_name(processName):
    pid_list = []
    # Iterate over all running processes
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['pid', 'name', 'create_time'])
            # Check if process name contains the given name string.
            if processName.lower() in pinfo['name'].lower():
                pid_list.append(pinfo.get('pid'))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return pid_list



#write key strokes into the log file, including key, action Press/release, and foreground app
def print_pressed_keys(e):
    global file_logs
    try:
        with open(os.devnull, 'w') as devnull:
            pid = int(sp.check_output(["xdotool", "getactivewindow", "getwindowpid"],stderr=devnull).decode("utf-8").strip())
        if (pid > 0):
            exeFirstPlane = psutil.Process(pid).name()
            text_event=str(e)
            text_event=text_event[14:-1]
            parts_text=text_event.split(' ')
            key=''.join(parts_text[i] for i in range(0,len(parts_text)-1))
            key=key.lower()
            press=parts_text[len(parts_text)-1]
            if press=='down':
                file_logs.write(str(current_time()) + ",KP,{0},{1}\n".format(key, exeFirstPlane))
            elif press=='up':
                file_logs.write(str(current_time()) + ",KR,{0},{1}\n".format(key, exeFirstPlane))
    except:
        pass


#Write mouse movement events into the log file
def on_move(x, y):
    global file_logs
    try:
        with open(os.devnull, 'w') as devnull:
            pid = int(sp.check_output(["xdotool", "getactivewindow", "getwindowpid"],stderr=devnull).decode("utf-8").strip())
        if (pid > 0):
            exeFirstPlane = psutil.Process(pid).name()
            file_logs.write(str(current_time()) + ",MM,{0},{1},{2}\n".format(x, y, exeFirstPlane))
    except:
        pass
        # file_logs.write(str(current_time()) + ",MM,{0},{1},{2}\n".format(x, y, "-"))



# Pynput listener functions disabled due to current error
"""
def on_press(key):
    try:
        with open(os.devnull, 'w') as devnull:
            pid = int(sp.check_output(["xdotool", "getactivewindow", "getwindowpid"],stderr=devnull).decode("utf-8").strip())
        if (pid[-1] > 0):
            exeFirstPlane = psutil.Process(pid[-1]).name()
            print(key)
            file_logs.write(str(current_time()) + ",KP,{0},{1}\n".format(key, exeFirstPlane))
    except:
        pass
        # file_logs.write(str(current_time()) + ",KP,{0},{1}\n".format(key, "-"))
def on_release(key):
    try:
        with open(os.devnull, 'w') as devnull:
            pid = int(sp.check_output(["xdotool", "getactivewindow", "getwindowpid"],stderr=devnull).decode("utf-8").strip())
        if (pid[-1] > 0):
            exeFirstPlane = psutil.Process(pid[-1]).name()
            file_logs.write(str(current_time()) + ",KR,{0},{1}\n".format(key, exeFirstPlane))
        #if (key == Key.f12):
        #    ListenerKeyboard.stop()
        #    ListenerMouse.stop()
    except:
        pass
        # file_logs.write(str(current_time()) + ",KR,{0},{1}\n".format(key, "-"))
"""

#Write mouse click events into the log file
def on_click(x, y, button, pressed):
    global file_logs
    try:
        with open(os.devnull, 'w') as devnull:
            pid = int(sp.check_output(["xdotool", "getactivewindow", "getwindowpid"],stderr=devnull).decode("utf-8").strip())
        exeFirstPlane = psutil.Process(pid).name()
        file_logs.write(
            str(current_time()) + ",MC,{0},{1},{2},{3},{4}\n".format(x, y, button, pressed, exeFirstPlane))
    except:
        pass
        # file_logs.write(str(current_time()) + ",MC,{0},{1},{2},{3},{4}\n".format(x, y, button, pressed, "-"))

#Write scrolling events into the log file
def on_scroll(x, y, dx, dy):
    global file_logs
    try:
        with open(os.devnull, 'w') as devnull:
            pid = int(sp.check_output(["xdotool", "getactivewindow", "getwindowpid"],stderr=devnull).decode("utf-8").strip())
        if (pid > 0):
            exeFirstPlane = psutil.Process(pid).name()
            file_logs.write(str(current_time()) + ",MS,{0},{1},{2},{3},{4}\n".format(x, y, dx, dy, exeFirstPlane))
    except:
        pass
        # file_logs.write(str(current_time()) + ",MS,{0},{1},{2},{3},{4}\n".format(x, y, dx, dy, "-"))

#Enable listeners for mouse
ListenerMouse = mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)
#Pynpyt keyboard listener disabled based on accents errors:
#https://github.com/moses-palmer/pynput/issues/118
#ListenerKeyboard = pynput.keyboard.Listener(on_press=on_press, on_release=on_release)


#Class implementing the keyboard event listener thread
class thread_keyboard(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        hook(print_pressed_keys)
        wait()

    def stop(self):
        pass


#Launching function
def launch():
    #Consts
    global pids
    global file_logs
    total_bytes_sent = 0
    total_bytes_recv = 0
    const_notification=3600000

    #Close possible open files and prepare output files
    file_logs.close()
    try:
        os.remove(path)
    except Exception as e:
        #print("ERROR" + str(e))
        pass
    file_logs = open(path, 'a')
    sys.stdout = open(path_logs+'/output', 'w')
    sys.stderr = open(path_logs+'/errors','w')

    # Thread launch for mouse and keyboard event listening
    #ListenerKeyboard.start()
    t=thread_keyboard(1,"keyboard_thread",1)
    if not t.is_alive():
        t.start()

    if not ListenerMouse.is_alive():
        ListenerMouse.start()

    #Get current time stamp
    mark_time = current_time()
    # Read window If no window size is saved, the default value is 60
    window = 60
    mark_notification=0
    if os.path.exists(path_logs + "/window"):
        file_window = open(path_logs + "/window", 'r')
        try:
            window = int(file_window.read())
        except:
            window = 60
        file_window.close()

    #While mouse listener threat is alive, execute the application logic
    #Instead of while true, keeping track of the mouse threat allows to detect failures and re-lauch the app
    while ListenerMouse.isAlive():

        #Read pids of active windows and get current process in foreground
        """EnumWindows(EnumWindowsProc(foreach_window), 0)"""
        read_window_pids()
        processs_aplication=0
        try:
            with open(os.devnull, 'w') as devnull:
                pid_current = int(sp.check_output(["xdotool", "getactivewindow", "getwindowpid"], stderr=devnull).decode(
                    "utf-8").strip())
            name_process_current = psutil.Process(pid_current).name()
            if not pid_current in pids:
                pids.insert(0, pid_current)
            processs_aplication = len(find_pids_by_name(name_process_current))

        except Exception as e:
            #print("ERROR" + str(e))
            name_process_current = "-"

        #Read cpu, memory for each process and in general
        cpu_per_process = {}
        memory_per_process = {}
        memory_total = 0
        cpu_total = 0
        for pid in pids:
            try:
                p = psutil.Process(pid)
                cpu_total_process = 0
                memory_total_process = 0
                for i in range(0, 5):
                    cpu_total_process += p.cpu_percent(0.2)
                cpu_total_process = round(cpu_total_process / 5, 2)
                for pid2 in find_pids_by_name(p.name()):
                    p = psutil.Process(pid2)
                    memory_total_process += p.memory_percent()
                p = psutil.Process(pid)
                cpu_per_process[p.name()] = cpu_total_process
                cpu_total += cpu_total_process
                memory_total_process = round(memory_total_process, 2)
                memory_per_process[p.name()] = memory_total_process
                memory_total += memory_total_process
            except:
                pass
        cpu_total_device = psutil.cpu_percent()

        #Read sent/received bytes
        red = psutil.net_io_counters()
        if total_bytes_recv == 0:
            total_bytes_recv = red.bytes_recv
        if total_bytes_sent == 0:
            total_bytes_sent = red.bytes_sent
        diff_bytes_recv = red.bytes_recv - total_bytes_recv
        diff_bytes_sent = red.bytes_sent - total_bytes_sent
        total_bytes_recv = red.bytes_recv
        total_bytes_sent = red.bytes_sent
        memory_total = round(memory_total, 2)
        file_logs_2 = open(path_apps, 'a')

        #Build app and resource usage log and write it to the log file
        if name_process_current != "-" and name_process_current in cpu_per_process.keys():
            file_logs_2.write(
                str(current_time()) + ",APPS,{0},{1},{2},{3},{4},{5},{6},{7},{8},{9}\n".format(len(pids),name_process_current,cpu_per_process[name_process_current],cpu_total,memory_per_process[name_process_current],memory_total,cpu_total_device,diff_bytes_recv,diff_bytes_sent,str(processs_aplication)))
            file_logs_2.close()
        pids = []

        # Check if the time window is over
        if mark_time + window * 1000 < current_time():
            # Update timestamp
            mark_time = current_time()

            #Close log file and call the function responsible of generating and sending the vector to the server
            #The server answers with the new time window duration in seconds
            file_logs.close()
            window = extract_features.extract_features(path, path_apps, window)

            # Save time window
            file_window = open(path_logs + "/window", 'w')
            file_window.write(str(window))
            file_window.close()

            # Reset log files
            #file_logs.close()
            try:
                os.remove(path)
                os.remove(path_apps)
            except Exception as e:
                #print("ERROR"+str(e))
                pass
            file_logs = open(path, 'a')

            # Get evaluation results
            result = extract_features.obtain_auth_puntuation()
            text_notification=""

            #Show notification
            if result == 999:
                text_notification="Sent training data."
            elif result == 500:
                text_notification="Unable to reach the server."
            else:
                text_notification="Evaluation result: " + str(result)
            if mark_notification+const_notification < current_time():
                mark_notification=current_time()
                try:
                    os.system("notify-send 'Authcode: "+str(text_notification)+"'")
                except Exception as e:
                    print("BEHAVIOURAL DATA SENT")

        time.sleep(2)
