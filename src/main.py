from PyQt5.QtWidgets import QApplication
from sys import exit as sys_exit
from ui import *

app, ui = QApplication([]), ui()
sys_exit(app.exec_())