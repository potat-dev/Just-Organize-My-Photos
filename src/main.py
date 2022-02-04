from PyQt5.QtWidgets import QApplication
from sys import exit as sys_exit

# импортируем свои функции
from ui import *

app, ui = QApplication([]), Ui()
sys_exit(app.exec_())