from PyQt5.QtWidgets import QApplication
from sys import exit as sys_exit
from app import *

app, ui = QApplication([]), app()
sys_exit(app.exec_())