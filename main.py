from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QFileDialog
from PyQt5.QtGui import QPixmap
from datetime import datetime
import os, sys, glob, math
from PyQt5 import QtCore
from PIL import Image
from ui import *

def convert_size(size_bytes):
   if size_bytes == 0: return "0"
   i = int(math.floor(math.log(size_bytes, 1024)))
   s = round(size_bytes / math.pow(1024, i), 2)
   return "%s %s" % (s, ("B", "KB", "MB", "GB")[i])

class Ui(QMainWindow):
    #TODO: вынести код в удобные красивые функции
    #TODO: реализовать алгоритм выбора папки для шортката

    def __init__(self):
        super(Ui, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setChildrenFocusPolicy(QtCore.Qt.NoFocus)
        self.ui.path_btn.clicked.connect(self.checkPath)
        self.ui.btn_next.clicked.connect(self.nextImage)
        self.ui.btn_prev.clicked.connect(self.prevImage)

        # variables
        self.image_id = 0
        self.im_count = 0
        self.image_list = []
        self.path = ""
        self.image_path = ""
        self.image = None

        self.show()

    def nextImage(self): self.changeImage(1)
    def prevImage(self): self.changeImage(-1)

    def setChildrenFocusPolicy(self, policy):
        def recursiveSetChildFocusPolicy (parentQWidget):
            for childQWidget in parentQWidget.findChildren(QtWidgets.QWidget):
                childQWidget.setFocusPolicy(policy)
                recursiveSetChildFocusPolicy(childQWidget)
        recursiveSetChildFocusPolicy(self.ui.centralwidget)

    def pickDirectory(self):
        return str(QFileDialog.getExistingDirectory(self, "Select Directory"))
    
    def checkPath(self): # currently not supporting RAW, ARW, ...
        self.path = self.pickDirectory()
        self.image_list = [item for i in [glob.glob(f"{self.path}\/*{ext}") for ext in ["jpg","jpeg","png"]] for item in i]
        self.im_count = len(self.image_list)
        self.image_id = 0
        self.ui.path_text.setText(f"path: {self.path} ({self.im_count} photo)")
        if self.im_count > 0:
            self.displayImg()

    def displayImg(self):
        if self.im_count > 0:
            self.image_path = self.image_list[self.image_id]
            if os.path.isfile(self.image_path):
                w, h = self.ui.graphicsView.width(), self.ui.graphicsView.height()
                scene = QtWidgets.QGraphicsScene(self)
                pixmap = QPixmap(self.image_path)
                item = QtWidgets.QGraphicsPixmapItem(pixmap.scaled(w, h, QtCore.Qt.KeepAspectRatio))
                scene.addItem(item)
                self.ui.graphicsView.setScene(scene)
                self.image = Image.open(self.image_path)
                self.ui.path_text.setText(f"File: {os.path.basename(self.image_path)}\nPath: {self.path}")
                self.ui.info_text.setText(
                    f"Image {self.image_id + 1} / {self.im_count}\n" +
                    f"Res: {' × '.join([str(i) for i in self.image.size])}\n" +
                    f"Size: {convert_size(os.path.getsize(self.image_path))}\n" +
                    f"Date: {datetime.fromtimestamp(os.path.getmtime(self.image_path)).strftime('%d.%m.%Y')}") # full: %d.%m.%Y %H:%M:%S

    def changeImage(self, order):
        self.image_id += order
        if self.image_id == self.im_count:
            self.image_id = 0
        elif self.image_id < 0:
            self.image_id = self.im_count-1
        self.displayImg()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_1:
            self.changeImage(1) # for test
        elif event.key() == QtCore.Qt.Key_2:
            self.changeImage(-1) # for test
        elif event.key() == QtCore.Qt.Key_Right:
            self.changeImage(1)
        elif event.key() == QtCore.Qt.Key_Left:
            self.changeImage(-1)
        # elif event.key() == QtCore.Qt.Key_Delete:
        # elif event.key() == QtCore.Qt.Key_0:
        # elif event.key() == QtCore.Qt.Key_Enter:
        # elif event.key() == QtCore.Qt.Key_Space:
        else:
            QMainWindow.keyPressEvent(self, event)


app = QApplication([])
ui = Ui()
sys.exit(app.exec_())