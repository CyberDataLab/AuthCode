AUTHCODE LINUX VERSION

In Linux, __init__.py has to be outside the logic_code folder in order to be able to import in __init__.py the other source files.

To build the executable use:
sudo pyinstaller --onefile __init__.py
