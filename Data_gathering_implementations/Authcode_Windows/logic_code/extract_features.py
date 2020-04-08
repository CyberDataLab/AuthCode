import os
import time
from pathlib import Path

import statistics
import requests
import math
from win32api import GetSystemMetrics

#URL and port where the server is located
urlServer = "http://155.54.95.234:5002"

home = Path.home()
path = str(home) + "\\Authcode"
path_idUser = path + "\\" + "idUser"


def get_userId():
    if os.path.exists(path_idUser):
        fichId = open(path_idUser, 'r')
        userId = fichId.read().split(':')[0]
        fichId.close()
    else:
        userId = "Undefined"
    return userId


def average(list):
    if len(list) == 0:
        return 0
    return round(sum(list) / len(list), 2)


def dev(list):
    if len(list) == 0 or len(list) == 1:
        return 0
    return round(statistics.stdev(list), 2)


def word_histogram(list):
    histogram = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0}
    for n in list:
        if n >= 11:
            histogram[11] += 1
        else:
            histogram[n] += 1
    return histogram


def average_dictionary_length(dictionary):
    dictionary_result = {}
    for k in dictionary.keys():
        dictionary_result[k] = average(dictionary[k])
    return dictionary_result


def cero_division(arg1, arg2):
    if arg1 == 0 or arg2 == 0:
        return 0
    return round(arg1 / arg2, 2)


def position_histogram(list):
    histogram = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}
    for n in list:
        histogram[n] += 1
    return histogram


def direction_histogram(list):
    histogram = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0}
    for n in list:
        histogram[n] += 1
    return histogram


def movement_length_histogram(list):
    histogram = {1: 0, 2: 0, 3: 0}
    for n in list:
        histogram[n] += 1
    return histogram


def get_screen_quadrant(x, y):
    xMax = GetSystemMetrics(0)
    yMax = GetSystemMetrics(1)
    x = float(x)
    y = float(y)
    if x < xMax / 3 and y < yMax / 3:
        return 1
    elif (xMax / 3 <= x < (xMax / 3) * 2) and y < yMax / 3:
        return 2
    elif (xMax / 3) * 2 <= x and y < yMax / 3:
        return 3
    elif x < xMax / 3 and (yMax / 3 <= y <= (yMax / 3) * 2):
        return 4
    elif (xMax / 3 <= x < (xMax / 3) * 2) and (yMax / 3 <= y <= (yMax / 3) * 2):
        return 5
    elif (xMax / 3) * 2 <= x and (yMax / 3 <= y <= (yMax / 3) * 2):
        return 6
    elif x < xMax / 3 and (yMax / 3) * 2 <= y:
        return 7
    elif (xMax / 3 <= x < (xMax / 3) * 2) and (yMax / 3) * 2 <= y:
        return 8
    elif (xMax / 3) * 2 <= x and (yMax / 3) * 2 <= y:
        return 9


def obtain_direction_angle(ax, ay, bx, by):
    dy = by - ay
    dx = bx - ax

    angle = math.degrees(math.atan2(dy, dx))

    if angle < 0:
        angle += 360
    if 0 <= angle < 45:
        return 1
    elif 45 <= angle < 90:
        return 2
    elif 90 <= angle < 135:
        return 3
    elif 135 <= angle < 180:
        return 4
    elif 180 <= angle < 225:
        return 5
    elif 225 <= angle < 270:
        return 6
    elif 270 <= angle < 315:
        return 7
    elif 315 <= angle:
        return 8


def movement_length(distancia):
    max_mov = math.sqrt(pow(GetSystemMetrics(0), 2) + pow(GetSystemMetrics(1), 2))

    if distancia < max_mov / 3:
        return 1
    elif max_mov / 3 <= distancia < 2 * max_mov / 3:
        return 2
    else:
        return 3


def distance_between_points(ax, ay, bx, by):
    dy = by - ay
    dx = bx - ax

    return math.sqrt(pow(dx, 2) + pow(dy, 2))


def extract_features(file_path, file_apps, window):
    """
    CONSTANTS FOR DOUBLE CLICK
    """
    CONSTANT_DOBLE_CLICK = 500
    CONSTANT_SUBWINDOW = 500

    """"
    Event counters
    """
    events_keyboard = 0
    events_mouse = 0

    """"
    Keyboard keys and calculated parameters
    """
    list_keys = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'to', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                        'j', 'k', 'l', 'm', 'n', 'ñ', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'ç']
    list_space = ['-', '_', '.', ',', '/','&', '+', '<', 'space', 'tab', 'enter','(',')','=','|','\\','#']
    length_word = 0  # logitud of the word current
    number_words = 0  # number of words in the window current
    list_length_words = []
    list_all_keys = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'to', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                          'j', 'k', 'l', 'm', 'n', 'ñ', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '´',
                          '`', "'", '"', 'ç', '^','º','@','$','%','&','/','(',')','=','|','windowsizquierda','crtl',
                          'mayusculas','bloqmayus', 'tab','º','ª','\\','#','esc','f1','f2','f3','f4','f5','f6','f7','f8',
                          'f9','f10','f11','f12','imppant','insert','supr', 'inicio', 'fin', 'repag','avpag','numlock',
                          '}','{','-', '_','.', ',', '[',']','*','<','>','space','tab','enter','ctrlderecha',
                          'rightshift','backspace','atlgr','alt','left','right','up','down','flechaderecha',
                          'flechaizquierda','flechaarriba', 'flechaabajo', '+']
    file = open(file_path, "r")
    #calculated features atributes

    time_mark = 0
    last_key_pressed = ''
    time_mark_last_press = 0  # Time stamp of the last key pressed
    total_keys_pressed = 0  # Number of keys pressed in the window of time
    total_keys_erase = 0  # Number of keys of erase pressed
    presses_per_key = {}  # Number of presses per key
    for t in list_all_keys:
        presses_per_key[t] = 0
    keys_pressed = []  # Keys pressed
    interval_time_presionar_keys = []  # Intervals of time in order of press of keys
    list_intervals_press_release_key = []  # Intervals of press y release each key
    marks_time_pressed = {}  # Time stamp when each key has been pressed per last vez
    for t in list_all_keys:
        marks_time_pressed[t] = 0
    intervals_press_release_per_key = {}  # List of time of presses of each key
    for t in list_all_keys:
        intervals_press_release_per_key[t] = []
    interval_digraph = {}  # time between two presses of all the keys
    for t in list_all_keys:
        for t2 in list_all_keys:
            interval_digraph[t + t2] = []
    digraph = {}  # press sequences of two keys
    for t in list_all_keys:
        for t2 in list_all_keys:
            digraph[t + t2] = 0

    """
    Mouse attributes
    """
    marks_time_click = {0: 0, 1: 0, 3: 0}
    interval_time_click = {0: [], 1: [], 2: [], 3: []}
    list_position_mouse = []
    # Last position X
    mark_x = 0
    # Last position Y
    mark_y = 0
    # List with the directions of the movements
    list_directions_movement = []
    # Position of the first event of movement inside of the subwindow
    mark_x_angle = 0
    mark_y_angle = 0
    # List for the distintas actions of the ratón
    list_actions_mouse = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}

    # Mouse auxiliar features
    drag = False
    last_action_mouse = ''
    time_mark_movement = 0
    interval_movement_click = []
    length_traveled = 0
    list_length_movement = []
    list_speeds_average = []
    list_speeds_average_directions = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: []}
    is_double_click = False
    time_mark_first_movement = 0
    previousDoubleClick = True
    """
    APPS VARS
    """
    list_number_apps = []
    list_name_apps = []
    cpu_per_process = {}
    ram_per_aplication = {}
    list_cpu_total = []
    list_ram_total = []
    bytes_recv = 0
    bytes_sent = 0
    time_first_plane_in_window = {}
    processes_per_aplication = {}
    """
    AUXILIARY VARS
    """
    start_subwindow = 0

    for line in file.readlines():
        line = line[:-1]  #  delete last \n char
        parts = line.split(",")
        time_mark = int(parts[0])
        event = parts[1]

        if start_subwindow == 0:
            start_subwindow = time_mark

        if time_mark > start_subwindow + CONSTANT_SUBWINDOW:
            list_length_movement.append(int(movement_length(length_traveled)))
            angle_direction = int(obtain_direction_angle(mark_x, mark_y, mark_x_angle, mark_y_angle))
            list_directions_movement.append(angle_direction)
            if (int(time_mark_movement) - int(time_mark_first_movement)) != 0:
                list_speeds_average.append(length_traveled / (int(time_mark_movement)
                                                                      - int(time_mark_first_movement)))
                list_speeds_average_directions[angle_direction].append(length_traveled /
                                                                              (int(time_mark_movement)
                                                                               - int(time_mark_first_movement)))
            length_traveled = 0
            time_mark_first_movement = 0
            start_subwindow = time_mark

        # event gestion
        if event == "KP":
            events_keyboard = events_keyboard + 1
            key = parts[2]
            key = key.replace('\'', '')
            if key in list_all_keys:
                if marks_time_pressed[key] == 0:
                    # Incrementar counters
                    total_keys_pressed = total_keys_pressed + 1
                    if key == 'backspace' or key == 'supr':
                        total_keys_erase = total_keys_erase + 1
                    presses_per_key[key] = presses_per_key[key] + 1

                    # Include key pressed to the list
                    keys_pressed.append(key)

                    # Include marks of time of press
                    marks_time_pressed[key] = time_mark
                    if time_mark_last_press != 0:
                        interval_time_presionar_keys.append(time_mark - time_mark_last_press)
                        interval_digraph[key + last_key_pressed].append(
                            time_mark - time_mark_last_press)
                        digraph[key + last_key_pressed] = digraph[key + last_key_pressed] + 1

                    # Restart variables of last key pressed
                    last_key_pressed = key
                    time_mark_last_press = time_mark

                    if key in list_keys:
                        length_word = length_word + 1
                    if (key in list_space) and length_word > 0:
                        number_words = number_words + 1
                        list_length_words.append(int(length_word))
                        length_word = 0
                    # print(start_window, " ", key," ",interval_time_keys_pressed)



        elif event == "KR":
            events_keyboard = events_keyboard + 1
            key = parts[2]
            key = key.replace('\'', '')
            if key in list_all_keys:
                if marks_time_pressed[key] != 0:
                    list_intervals_press_release_key.append(time_mark - marks_time_pressed[key])
                    intervals_press_release_per_key[key].append(time_mark - marks_time_pressed[key])
                    marks_time_pressed[key] = 0


        elif event == "MM":
            events_mouse = events_mouse + 1
            time_mark_movement = time_mark
            last_action_mouse = "MM"
            list_position_mouse.append(get_screen_quadrant(parts[2], parts[3]))

            if (start_subwindow == time_mark):
                mark_x_angle = int(parts[2])
                mark_y_angle = int(parts[3])

            if time_mark_first_movement == 0:
                time_mark_first_movement = time_mark

            if drag:
                list_actions_mouse[5] += 1
            else:
                list_actions_mouse[4] += 1

            length_traveled += distance_between_points(int(parts[2]), int(parts[3]), mark_x, mark_y)

            mark_x = int(parts[2])
            mark_y = int(parts[3])


        elif event == "MS":
            last_action_mouse = "MS"
            events_mouse = events_mouse + 1
            if drag:
                list_actions_mouse[5] += 1
            else:
                list_actions_mouse[3] += 1
            list_position_mouse.append(get_screen_quadrant(parts[2], parts[3]))


        elif event == "MC":
            events_mouse = events_mouse + 1
            list_position_mouse.append(get_screen_quadrant(parts[2], parts[3]))
            button = str(parts[4])
            press = str(parts[5])

            if last_action_mouse == "MM":
                interval_movement_click.append(time_mark - time_mark_movement)

            if button == "Button.left":
                if press == "False":
                    if not is_double_click:
                        interval_time_click[0].append(time_mark - marks_time_click[0])
                        drag = False
                    else:
                        interval_time_click[2].append(time_mark - marks_time_click[0])
                        if len(interval_time_click[0]) != 0:
                            interval_time_click[0].pop()
                else:
                    if previousDoubleClick or marks_time_click[0] + CONSTANT_DOBLE_CLICK < time_mark:
                        list_actions_mouse[0] += 1
                        marks_time_click[0] = time_mark
                        is_double_click = False
                        previousDoubleClick = False
                        drag = True
                    else:
                        list_actions_mouse[2] += 1
                        if (list_actions_mouse[0] > 0):
                            list_actions_mouse[0] -= 1
                        marks_time_click[0] = time_mark
                        is_double_click = True
                        previousDoubleClick = True
            elif button == "Button.right":
                if press == "False":
                    if marks_time_click[1] != 0:
                        interval_time_click[1].append(time_mark - marks_time_click[1])
                else:
                    list_actions_mouse[1] += 1
                    marks_time_click[1] = time_mark
            elif button == "Button.middle":
                if press == "True":
                    marks_time_click[3] = time_mark
                    list_actions_mouse[6] += 1
                else:
                    if marks_time_click[3] != 0:
                        interval_time_click[3].append(time_mark - marks_time_click[3])
            last_action_mouse = "MC"

    file.close()
    file = open(file_apps, 'r')
    last_app = ""
    mark_last_app = 0
    for line in file.readlines():
        line = line[:-1]  #  delete jump \n key
        parts = line.split(",")
        time_mark = int(parts[0])
        event = parts[1]
        if event == "APPS":
            number_apps = int(parts[2])
            list_number_apps.append(number_apps)
            name_process_current = parts[3]
            list_name_apps.append(name_process_current)
            cpu_process_current = float(parts[4])
            if name_process_current not in cpu_per_process.keys():
                cpu_per_process[name_process_current] = []
            cpu_per_process[name_process_current].append(cpu_process_current)

            ram_aplication_current = float(parts[6])
            if name_process_current not in ram_per_aplication.keys():
                ram_per_aplication[name_process_current] = []
            ram_per_aplication[name_process_current].append(ram_aplication_current)

            ram_total_current = float(parts[7])
            list_ram_total.append(ram_total_current)
            cpu_total_current = float(parts[8])
            list_cpu_total.append(cpu_total_current)
            diff_bytes_recv = float(parts[9])
            bytes_recv += diff_bytes_recv
            diff_bytes_sent = float(parts[10])
            bytes_sent += diff_bytes_sent

            n_processes = int(parts[11])
            if name_process_current not in processes_per_aplication.keys():
                processes_per_aplication[name_process_current] = []
            processes_per_aplication[name_process_current].append(n_processes)

            if name_process_current != last_app:
                if name_process_current not in time_first_plane_in_window.keys():
                    time_first_plane_in_window[name_process_current] = 0
                if mark_last_app != 0:
                    time_first_plane_in_window[last_app] += time_mark - mark_last_app
                last_app = name_process_current
                mark_last_app = time_mark
    if not (last_app=='' or time_mark==0 or mark_last_app==0):
        time_first_plane_in_window[last_app] += time_mark - mark_last_app
    file.close()

    # Save last word
    if length_word > 0:
        number_words += 1
        list_length_words.append(int(length_word))

    #SAVE VECTOR AND SEND IT TO THE SERVER
    current_time = lambda: int(time.time() * 1000)
    time_mark= current_time()
    
    # Keyboard vector part generation
    vector = str(time_mark) + "," + str(total_keys_pressed) + "," + str(total_keys_erase) + "," + str(
        cero_division(total_keys_erase, total_keys_pressed)) + "," + str(
        average(interval_time_presionar_keys)) + "," + str(
        dev(interval_time_presionar_keys)) + "," + str(
        average(list_intervals_press_release_key)) + "," + str(
        dev(list_intervals_press_release_key)) + "," + str(number_words) + "," + str(
        average(list_length_words)) + "," + str(dev(list_length_words)) + ","
    for v in word_histogram(list_length_words).values():
        vector = vector + str(v) + ","

    for v in presses_per_key.values():
        vector = vector + str(v) + ","

    for v in average_dictionary_length(intervals_press_release_per_key).values():
        vector = vector + str(v) + ","

    for v in digraph.values():
        vector = vector + str(v) + ","

    for v in average_dictionary_length(interval_digraph).values():
        vector = vector + str(v) + ","

    # Mouse vector part generation
    mouse_vector = str(average(interval_time_click[0])) + ',' + str(average(interval_time_click[1])) + ',' + str(
        average(interval_time_click[2])) + ',' + str(average(interval_time_click[3])) + ',' + str(
        dev(interval_time_click[0])) + ',' + str(dev(interval_time_click[1])) + ',' + str(
        dev(interval_time_click[2])) + ',' + str(dev(interval_time_click[3])) + ','

    for v in list_actions_mouse.values():
        mouse_vector += str(v) + ','

    for v in position_histogram(list_position_mouse).values():
        mouse_vector += str(v) + ','

    for v in direction_histogram(list_directions_movement).values():
        mouse_vector += str(v) + ','

    for v in movement_length_histogram(list_length_movement).values():
        mouse_vector += str(v) + ','

    mouse_vector += str(average(interval_movement_click)) + ',' + str(average(list_speeds_average) * 1000) + ','

    for v in list_speeds_average_directions.values():
        mouse_vector += str(average(v) * 1000) + ','

    vector += mouse_vector

    # App/resource usage vector part
    vector += str(average(list_number_apps)) + ","
    aplication_current = ""
    penultimate_aplication = ""
    changes_of_aplication = 0
    for app in list_name_apps:
        if app != aplication_current:
            penultimate_aplication = aplication_current
            aplication_current = app
            if penultimate_aplication != "":
                changes_of_aplication += 1
    if aplication_current!='':
        vector += aplication_current + ','
        vector += penultimate_aplication + ','
        vector += str(changes_of_aplication) + ','
        if penultimate_aplication == "":
            vector += str(window) + ','
        else:
            vector += str(round(time_first_plane_in_window[aplication_current] / 1000, 2)) + ','
        vector += str(average(processes_per_aplication[aplication_current])) + ','
        vector += str(dev(processes_per_aplication[aplication_current])) + ','
        vector += str(average(cpu_per_process[aplication_current])) + ","
        vector += str(dev(cpu_per_process[aplication_current])) + ","
        vector += str(average(list_cpu_total)) + ","
        vector += str(dev(list_cpu_total)) + ","
        vector += str(average(ram_per_aplication[aplication_current])) + ','
        vector += str(dev(ram_per_aplication[aplication_current])) + ','
        vector += str(average(list_ram_total)) + ','
        vector += str(dev(list_ram_total)) + ','
        vector += str(bytes_recv) + ','
        vector += str(bytes_sent) + ','

        # Delete end comma
        vector = vector[:-1] + "\n"

        print(mouse_vector)
        print(vector)
        userId = get_userId()
        try:
            if os.path.exists(path + "\\" + "unsent_vectors.txt"):
                file = open(path + "\\" + "unsent_vectors.txt", 'r')
                for line in file.readlines():
                    requests.post(urlServer + "/pc/" + userId, data=line.encode("utf-8"))
                file.close()
                os.remove(path + "\\" + "unsent_vectors.txt")
            response = requests.post(urlServer + "/pc/" + userId, data=vector.encode("utf-8"))
            return int(response.text)
        except:
            file = open(path + "\\" + "unsent_vectors.txt", 'to')
            file.write(vector)
            file.close()
            return window


def obtain_auth_puntuation():
    try:
        userId = get_userId()
        response = requests.get(urlServer + "/pc/" + userId)
        return float(response.text)
    except:
        return 500
