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
    #TODO: добавить кнопки < > и удалить

    image_id = 0
    im_count = 0
    image_list = []
    path = ""
    image_path = ""
    image = None

    def __init__(self):
        super(Ui, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setChildrenFocusPolicy(QtCore.Qt.NoFocus)
        self.ui.path_btn.clicked.connect(self.checkPath)
        self.show()

    def setChildrenFocusPolicy (self, policy):
        def recursiveSetChildFocusPolicy (parentQWidget):
            for childQWidget in parentQWidget.findChildren(QtWidgets.QWidget):
                childQWidget.setFocusPolicy(policy)
                recursiveSetChildFocusPolicy(childQWidget)
        recursiveSetChildFocusPolicy(self.ui.centralwidget)
    
    def checkPath(self): # currently not supporting RAW, ARW, ...
        self.path = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
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
                    f"Date: {datetime.fromtimestamp(os.path.getmtime(self.image_path)).strftime('%d.%m.%Y')}" # full: %d.%m.%Y %H:%M:%S
                )

    def nextImage(self, order):
        self.image_id += order
        if self.image_id == self.im_count:
            self.image_id = 0
        elif self.image_id < 0:
            self.image_id = self.im_count-1

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_1:
            self.nextImage(1) # for test
            self.displayImg() # for test
            self.ui.pushButton_1.animateClick()
        elif event.key() == QtCore.Qt.Key_2:
            self.nextImage(-1) # for test
            self.displayImg()  # for test
            self.ui.pushButton_2.animateClick()
        elif event.key() == QtCore.Qt.Key_Right:
            self.nextImage(1)
            self.displayImg()
        elif event.key() == QtCore.Qt.Key_Left:
            self.nextImage(-1)
            self.displayImg()
        elif event.key() == QtCore.Qt.Key_3:
            self.ui.pushButton_3.animateClick()
        elif event.key() == QtCore.Qt.Key_4:
            self.ui.pushButton_4.animateClick()
        elif event.key() == QtCore.Qt.Key_5:
            self.ui.pushButton_5.animateClick()
        elif event.key() == QtCore.Qt.Key_6:
            self.ui.pushButton_6.animateClick()
        elif event.key() == QtCore.Qt.Key_7:
            self.ui.pushButton_7.animateClick()
        elif event.key() == QtCore.Qt.Key_8:
            self.ui.pushButton_8.animateClick()
        elif event.key() == QtCore.Qt.Key_9:
            self.ui.pushButton_9.animateClick()
        elif event.key() == QtCore.Qt.Key_0:
            self.ui.pushButton_0.animateClick()
        elif event.key() == QtCore.Qt.Key_Enter:
            self.ui.pushButton_e.animateClick()
        elif event.key() == QtCore.Qt.Key_Space:
            self.ui.pushButton_s.animateClick() 
        else:
            QMainWindow.keyPressEvent(self, event)


app = QApplication([])
ui = Ui()
sys.exit(app.exec_())