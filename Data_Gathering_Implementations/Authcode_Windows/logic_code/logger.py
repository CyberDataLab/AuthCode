import time
import win32gui
from win32gui import GetForegroundWindow
import psutil
import win32process
import pynput
import os
from win10toast import ToastNotifier
import win32con
import threading

from logic_code import extract_features
from pathlib import Path
import ctypes
from logic_code.keyboard import *

# Lamba to obtain milisecond timemark
current_time = lambda: int(time.time() * 1000)

# Generate work directory
home = Path.home()
path_logs = str(home) + "\\Authcode"
if not os.path.exists(path_logs):
    os.mkdir(path_logs)

# Generate temporal log files
path = path_logs + "\\mouse_keyboard_log_servicio.txt"
if os.path.exists(path):
    os.remove(path)
path_apps= path_logs + "\\apps_log_servicio.txt"
if os.path.exists(path_apps):
    os.remove(path_apps)
file_logs = open(path, 'a')

#Variables for process and application information gathering
EnumWindows = ctypes.windll.user32.EnumWindows
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
GetWindowText = ctypes.windll.user32.GetWindowTextW
GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
IsWindowVisible = ctypes.windll.user32.IsWindowVisible

pids = []


def foreach_window(hwnd, lParam):
    global pids
    if IsWindowVisible(hwnd):
        length = GetWindowTextLength(hwnd)
        if length != 0:
            buff = ctypes.create_unicode_buffer(length + 1)
            GetWindowText(hwnd, buff, length + 1)
            hwnd = win32gui.FindWindow(None, buff.value)
            long_window = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
            if long_window >= 0:
                threadid, pid = win32process.GetWindowThreadProcessId(hwnd)
                pids.append(pid)
    return True


def find_pids_by_name(processName):
    pid_list = []
    # Iterate over all running process
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['pid', 'name', 'create_time'])
            # Check if process name contains the given name string.
            if processName.lower() in pinfo['name'].lower():
                pid_list.append(pinfo.get('pid'))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return pid_list



# Pynput listener functions disabled due to current error
"""
def on_press(key):
    try:
        pid = win32process.GetWindowThreadProcessId(GetForegroundWindow())
        if (pid[-1] > 0):
            exePrimerPlano = psutil.Process(pid[-1]).name()
            print(key)
            file_logs.write(str(current_time()) + ",KP,{0},{1}\n".format(key, exePrimerPlano))
    except:
        pass
        # file_logs.write(str(current_time()) + ",KP,{0},{1}\n".format(key, "-"))


def on_release(key):
    try:
        pid = win32process.GetWindowThreadProcessId(GetForegroundWindow())
        if (pid[-1] > 0):
            exePrimerPlano = psutil.Process(pid[-1]).name()
            file_logs.write(str(current_time()) + ",KR,{0},{1}\n".format(key, exePrimerPlano))
        #if (key == Key.f12):
        #    ListenerKeyboard.stop()
        #    ListenerMouse.stop()

    except:
        pass
        # file_logs.write(str(current_time()) + ",KR,{0},{1}\n".format(key, "-"))

"""

#write key strokes into the log file, including key, action Press/release, and foreground app
def print_pressed_keys(e):
    try:
        pid = win32process.GetWindowThreadProcessId(GetForegroundWindow())
        if (pid[-1] > 0):
            foreground_exec = psutil.Process(pid[-1]).name()
            text_event=str(e)
            text_event=text_event[14:-1]
            text_parts=text_event.split(' ')
            key=''.join(text_parts[i] for i in range(0,len(text_parts)-1))
            key=key.lower()
            press=text_parts[len(text_parts)-1]
            if press=='down':
                file_logs.write(str(current_time()) + ",KP,{0},{1}\n".format(key, foreground_exec))
            elif press=='up':
                file_logs.write(str(current_time()) + ",KR,{0},{1}\n".format(key, foreground_exec))
    except:
        pass

#Write mouse movement events into the log file
def on_move(x, y):
    try:
        pid = win32process.GetWindowThreadProcessId(GetForegroundWindow())
        if (pid[-1] > 0):
            foreground_exec = psutil.Process(pid[-1]).name()
            file_logs.write(str(current_time()) + ",MM,{0},{1},{2}\n".format(x, y, foreground_exec))
    except:
        pass
        # file_logs.write(str(current_time()) + ",MM,{0},{1},{2}\n".format(x, y, "-"))

#Write mouse click events into the log file
def on_click(x, y, button, pressed):
    try:
        pid = win32process.GetWindowThreadProcessId(GetForegroundWindow())
        foreground_exec = psutil.Process(pid[-1]).name()
        file_logs.write(
            str(current_time()) + ",MC,{0},{1},{2},{3},{4}\n".format(x, y, button, pressed, foreground_exec))
    except:
        pass
        # file_logs.write(str(current_time()) + ",MC,{0},{1},{2},{3},{4}\n".format(x, y, button, pressed, "-"))

#Write scrolling events into the log file
def on_scroll(x, y, dx, dy):
    try:
        pid = win32process.GetWindowThreadProcessId(GetForegroundWindow())
        if (pid[-1] > 0):
            foreground_exec = psutil.Process(pid[-1]).name()
            file_logs.write(str(current_time()) + ",MS,{0},{1},{2},{3},{4}\n".format(x, y, dx, dy, foreground_exec))
    except:
        pass
        # file_logs.write(str(current_time()) + ",MS,{0},{1},{2},{3},{4}\n".format(x, y, dx, dy, "-"))


ListenerMouse = pynput.mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)
#ListenerKeyboard = pynput.keyboard.Listener(on_press=on_press, on_release=on_release)

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
    global pids
    global file_logs
    toast_notifier = ToastNotifier()

    # Thread launch for mouse and keyboard event listening
    #ListenerKeyboard.start()
    t=thread_keyboard(1,"keyboard_thread",1)
    if not t.is_alive():
        t.start()

    if not ListenerMouse.is_alive():
        ListenerMouse.start()
    
    timestamp = current_time()
    # Read window. If no window size is saved, the default value is 60
    window = 60
    total_bytes_sent = 0
    total_bytes_recv = 0
    constant_notification=3600000
    mark_notification=0
    if os.path.exists(path_logs + "\\window"):
        file_window = open(path_logs + "\\window", 'r')
        try:
            window = int(file_window.read())
        except:
            window = 60
        file_window.close()


    #While mouse listener threat is alive, execute the application logic
    #Instead of while true, keeping track of the mouse threat allows to detect failures and re-lauch the app
    while ListenerMouse.isAlive():

        #Read pids of active windows and get current process in foreground
        EnumWindows(EnumWindowsProc(foreach_window), 0)
        processs_aplication=0
        try:
            pid_current = win32process.GetWindowThreadProcessId(GetForegroundWindow())
            name_process_current = psutil.Process(pid_current[-1]).name()
            if not pid_current[-1] in pids:
                pids.insert(0, pid_current[-1])
            processs_aplication = len(find_pids_by_name(name_process_current))

        except:
            name_process_current = "-"

        # Read cpu, memory for each process and in general
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
        file_logs_apps_resources = open(path_apps, 'a')

        #Build app and resource usage log and write it to the log file
        if name_process_current != "-" and name_process_current in cpu_per_process.keys():
            file_logs_apps_resources.write(
                str(current_time()) + ",APPS,{0},{1},{2},{3},{4},{5},{6},{7},{8},{9}\n".format(len(pids),name_process_current,cpu_per_process[name_process_current],cpu_total,memory_per_process[name_process_current],memory_total,cpu_total_device,diff_bytes_recv,diff_bytes_sent,str(processs_aplication)))
            file_logs_apps_resources.close()
        pids = []

        # Check if the time window is over
        if timestamp + window * 1000 < current_time():
            # Update timestamp
            timestamp = current_time()

            # Close log file and call the function responsible of generating and sending the vector to the server
            # The server answers with the new time window duration in seconds
            file_logs.close()
            window = extract_features.extract_features(path, path_apps, window)

            # Save time window
            file_window = open(path_logs + "\\window", 'w')
            file_window.write(str(window))
            file_window.close()

            # Restart file logs
            #file_logs.close()
            try:
                os.remove(path)
                os.remove(path_apps)
            except:
                pass
            file_logs = open(path, 'a')

            # Get evaluation results
            result = extract_features.obtain_auth_puntuation()
            text_notification = ""

            # Show notification
            if result == 999:
                text_notification = "Sent training data."
            elif result == 500:
                text_notification = "Unable to reach the server."
            else:
                text_notification = "Evaluation result: " + str(result)
                #if result==4:
                    #ctypes.windll.user32.LockWorkStation()
            if mark_notification+constant_notification < current_time():
                mark_notification=current_time()
                toast_notifier.show_toast("Authcode",text_notification,icon_path="authcode4.ico")
        time.sleep(2)
