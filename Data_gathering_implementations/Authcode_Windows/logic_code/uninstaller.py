import os
import shutil
import time
from pathlib import Path
import ctypes, sys
import psutil

def find_pids_by_name(processName):
    pid_list = []
    # Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['pid', 'name', 'create_time'])
            # Check if process name contains the given name string.
            if processName.lower() in pinfo['name'].lower():
                pid_list.append(pinfo.get('pid'))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return pid_list


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


if __name__=='__main__':
    if is_admin():
        pids = find_pids_by_name("logger.exe")
        for pid in pids:
            os.kill(pid, 9)

        time.sleep(3)

        home = Path.home()
        path = str(home) + "\\Authcode"
        if os.path.exists(path):
            shutil.rmtree(path)

        program_files = os.environ["ProgramFiles"]
        path_program = program_files + "\\Authcode"
        print(path_program)
        if os.path.exists(path_program):
            shutil.rmtree(path_program)

        program_files = os.environ["ProgramFiles(x86)"]
        path_program = program_files + "\\Authcode"
        print(path_program)
        if os.path.exists(path_program):
            shutil.rmtree(path_program)

        print("Program uninstalled successfully. / Programa desinstalado correctamente.")
        input("Press enter to exit. / Pulsa enter para salir. ;)")
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
