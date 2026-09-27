import GUI
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
import sys
import subprocess
import os

backend_process = None

def start_backend():
            global backend_process
            if getattr(sys, 'frozen', False):
                base_path = os.path.dirname(sys.executable)
            else:
                base_path = os.path.dirname(__file__)

            backend_path = os.path.join(
                        base_path, "Backend.exe"
            )
            backend_process = subprocess.Popen(
                                             [backend_path],
                                             creationflags=subprocess.CREATE_NO_WINDOW
                                 )

def close_app():
        global backend_process
        try: 
             requests.post("http://127.0.0.1:8000/shutdown")
        except Exception:
            print("Server could not be closed!")

        if backend_process and backend_process.poll():
             
             backend_process.terminate()
             backend_process.wait()


import time
import requests

def wait_for_backend():

    for i in range(20):
        try:
            r = requests.get("http://127.0.0.1:8000/")
            if r.status_code == 200:
                return True
        except:
            pass

        time.sleep(0.5)

    return False

try:
    start_backend()

    if not wait_for_backend():
        raise RuntimeError("Server couldn´t be started")
    
    app = QApplication(sys.argv)
    
    #Icon
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    appIcon = app_icon = os.path.join(BASE_DIR, "Icons", "icon1.png")
    app.setWindowIcon(QIcon(appIcon))
    
    
    app.setStyleSheet("""
                     QPushButton { 
                        min-width: 200px;
                        min-height: 30px;
                        max-width: 200px;
                        max-height: 30px;
                        }
                     QLineEdit{
                        min-width: 100px;
                        min-height: 30px;
                        max-width: 100px;
                        max-height: 30px;
                                }""")
        
    window = GUI.LoginWindow()
    window.show()
    
    app.exec()
finally:
    close_app()