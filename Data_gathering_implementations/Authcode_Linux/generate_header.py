def word_histogram(list):
    histogram = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0}
    for n in list:
        if n >= 11:
            histogram[11] += 1
        else:
            histogram[n] += 1
    return histogram

def position_histogram(list):
    histogram = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}
    for n in list:
        histogram[n] += 1
    return histogram
def mean(list):
    if len(list) == 0:
        return 0
    return round(sum(list) / len(list), 2)

def average_dictionaty_list(dictionary):
    output_dictionary = {}
    for k in dictionary.keys():
        output_dictionary[k] = mean(dictionary[k])
    return output_dictionary

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


list_length_words = []
list_all_keys = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                      'j', 'k', 'l', 'm', 'n', 'ñ', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '´',
                      '`', "'", '"', 'ç', '^', 'º', '@', '$', '%', '&', '/', '(', ')', '=', '|', 'leftwindows',
                      'crtl',
                      'shift', 'capslock', 'tab', 'º', 'ª', '\\', '#', 'esc', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6',
                      'f7', 'f8',
                      'f9', 'f10', 'f11', 'f12', 'PrtSc', 'insert', 'supr', 'home', 'ind', 'pageup', 'pagedown',
                      'numlock',
                      '}', '{', '-', '_', '.', ',', '[', ']', '*', '<', '>', 'space', 'tab', 'inter', 'rightctrl',
                      'rightshift', 'backspace', 'atlgr', 'alt', 'left', 'right', 'up', 'down', 'rightarrow',
                      'leftarrow', 'uparrow', 'downarrow', '+']

presses_per_key = {}
for t in list_all_keys:
    presses_per_key[t] = 0
keys_presionadas = []
interval_time_presionar_keys = []
list_intervals_press_release_key = []
marks_time_presionado = {}
for t in list_all_keys:
    marks_time_presionado[t] = 0
intervals_press_release_per_key = {}
for t in list_all_keys:
    intervals_press_release_per_key[t] = []
interval_digraph = {}
for t in list_all_keys:
    for t2 in list_all_keys:
        interval_digraph[t + t2] = []
digraph = {}
for t in list_all_keys:
    for t2 in list_all_keys:
        digraph[t + t2] = 0

"""
MOUSE VARIABLES 
"""
marks_time_click = {0: 0, 1: 0, 3: 0}
interval_time_click = {0: [], 1: [], 2: [], 3: []}
list_posicion_mouse = []
list_directions_movement = []
list_actions_mouse = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
interval_movement_click = []
list_length_movement = []
list_speeds_average_directions = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: []}


header=""
header+="Time_stamp,"
header+="keystroke_counter,"
header+="erase_keys_counter,"
header+="erase_keys_percentage,"
header+="press_press_average_interval,"
header+="press_press_stddev_interval,"
header+="press_release_average_interval,"
header+="press_release_stddev_interval,"
header+="word_counter,"
header+="word_average_length,"
header+="word_stddev_length,"
for v in word_histogram(list_length_words).keys():
    header+="word_length_"+str(v)+","

for v in presses_per_key.keys():
    v=v.replace(",","comma")
    header += "keystrokes_key_"+str(v)+","

for v in intervals_press_release_per_key.keys():
    v=v.replace(",","comma")
    header += "press_release_average_"+str(v)+","

for v in digraph.keys():
    v=v.replace(",","comma")
    header += "digraph_usage_"+str(v)+","

for v in digraph.keys():
    v=v.replace(",","comma")
    header += "digraph_average_time"+str(v)+","

for v in range(0,4):
    header += "click_speed_average_"+str(v)+","

for v in range(0,4):
    header += "click_speed_stddev_"+str(v)+","

for v in list_actions_mouse.keys():
    header+="mouse_action_counter_"+str(v)+","

for v in position_histogram(list_posicion_mouse).keys():
    header+="mouse_position_histogram_"+str(v)+","

for v in direction_histogram(list_directions_movement).keys():
    header+="mouse_movement_direction_histogram_"+str(v)+","

for v in movement_length_histogram(list_length_movement).keys():
    header+="mouse_movement_length_histogram_"+str(v)+","

header+="mouse_average_movement_duration,"
header += "mouse_average_movement_speed,"

for v in list_speeds_average_directions.keys():
    header+="mouse_average_movement_speed_direction_"+str(v)+","

header += "active_apps_average,"
header += "current_app,"
header += "penultimate_app,"
header += "changes_between_apps,"
header += "current_app_foreground_time,"
header += "current_app_average_processes,"
header += "current_app_stddev_processes,"
header += "current_app_average_cpu,"
header += "current_app_stddev_cpu,"
header += "system_average_cpu,"
header += "system_stddev_cpu,"
header += "current_app_average_mem,"
header += "current_app_stddev_mem,"
header += "system_average_mem,"
header += "system_stddev_mem,"
header += "received_bytes,"
header += "sent_bytes,"
header += "USER\n"

fich=open("header.txt","w")
fich.write(header)
fich.close()

print(len(header.split(",")))
