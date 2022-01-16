from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore
import os, sys, glob
from ui import *

class Ui(QMainWindow):
    image_id = 0
    im_count = 0
    image_list = []
    path = ""

    # def setChildrenFocusPolicy(self, policy):
    #     def recursiveSetChildFocusPolicy (parentQWidget):
    #         for childQWidget in parentQWidget.findChildren():
    #             childQWidget.setFocusPolicy(policy)
    #             recursiveSetChildFocusPolicy(childQWidget)
    #     recursiveSetChildFocusPolicy(self)

    def __init__(self):
        super(Ui, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setChildrenFocusPolicy(QtCore.Qt.NoFocus)

        self.ui.pushButton.clicked.connect(self.checkPath)
        # QtGui.qApp.installEventFilter(self)

        # self.setWindowFlags(self.windowFlags() |
        #     QtCore.Qt.WindowStaysOnTopHint |
        #     QtCore.Qt.FramelessWindowHint)

        self.show()

    def setChildrenFocusPolicy (self, policy):
        def recursiveSetChildFocusPolicy (parentQWidget):
            for childQWidget in parentQWidget.findChildren(QtWidgets.QWidget):
                childQWidget.setFocusPolicy(policy)
                recursiveSetChildFocusPolicy(childQWidget)
        recursiveSetChildFocusPolicy(self.ui.centralwidget)
    
    def checkPath(self):
        self.path = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.image_list = [item for i in [glob.glob(f"{self.path}\/*{ext}") for ext in ["jpg","jpeg","png"]] for item in i]
        self.im_count = len(self.image_list)
        self.image_id = 0
        self.ui.label_2.setText(f"path: {self.path} ({self.im_count} photo)")
        if self.im_count > 0:
            self.displayImg()

    def displayImg(self):
        if os.path.isfile(self.image_list[self.image_id]):
            w, h = self.ui.graphicsView.width(), self.ui.graphicsView.height()
            scene = QtWidgets.QGraphicsScene(self)
            pixmap = QPixmap(self.image_list[self.image_id])
            item = QtWidgets.QGraphicsPixmapItem(pixmap.scaled(w, h, QtCore.Qt.KeepAspectRatio))
            scene.addItem(item)
            self.ui.graphicsView.setScene(scene)
            self.ui.label.setText(f"image {self.image_id} / {self.im_count}")

    def nextImage(self, order):
        self.image_id += order
        if self.image_id == self.im_count:
            self.image_id = 0
        elif self.image_id < 0:
            self.image_id = self.im_count-1

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_1:
            self.nextImage(1)
            self.displayImg()
        elif event.key() == QtCore.Qt.Key_2:
            self.nextImage(-1)
            self.displayImg()
        elif event.key() == QtCore.Qt.Key_Right:
            self.nextImage(1)
            self.displayImg()
        elif event.key() == QtCore.Qt.Key_Left:
            self.nextImage(-1)
            self.displayImg()
        elif event.key() == QtCore.Qt.Key_3:
            pass
        elif event.key() == QtCore.Qt.Key_4:
            pass
        elif event.key() == QtCore.Qt.Key_5:
            pass
        elif event.key() == QtCore.Qt.Key_6:
            pass
        elif event.key() == QtCore.Qt.Key_7:
            pass
        elif event.key() == QtCore.Qt.Key_8:
            pass
        elif event.key() == QtCore.Qt.Key_9:
            pass
        elif event.key() == QtCore.Qt.Key_0:
            pass
        elif event.key() == QtCore.Qt.Key_Enter:
            pass
        elif event.key() == QtCore.Qt.Key_Space:
            pass 
        else:
            QMainWindow.keyPressEvent(self, event)
    
    # def resizeEvent(self, event):
    #     if not self.graphicsView.pixmap().isNull():
    #         self.fitInView(self.graphicsView, QtCore.Qt.KeepAspectRatio)
    #     super(Ui, self).resizeEvent(event)
    # def keyPressEvent(self, event):
		#     if event.key() == Qt.Key_Space:
		#     	self.test_method()

    # def test_method(self):
	  #   	print('Space key pressed')


app = QApplication([])
ui = Ui()
sys.exit(app.exec_())


# from PyQt5 import uic, QtWidgets
# from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QDialog, QGraphicsPixmapItem, QGraphicsScene
# from PyQt5.QtGui import QPixmap
# from PIL import Image
# import glob
# import sys

# Form, _ = uic.loadUiType("main.ui")

# class Ui(QMainWindow, Form):
#   def __init__(self):
#     super(Ui, self).__init__()
#     self.setupUi(self)

#     self.pushButton.clicked.connect(self.test)

#   def test(self):
#     path = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
#     print(path)
#     image_list = [item for i in [glob.glob(f"{path}/*{ext}") for ext in ["jpg","jpeg","png"]] for item in i]
#     print(image_list)
#     self.displayImg(image_list[0])

#   def displayImg(self, image_path):
#     pix = QPixmap(image_path)
#     item = QGraphicsPixmapItem(pix)
#     scene = QGraphicsScence(self)
#     scene.addItem(item)
#     self.graphicsView.setScene(scene)
  
# app = QApplication([])
# window = Ui()
# window.show()
# sys.exit(app.exec_())

# # app = QApplication([])
# # window = Window()
# # form = Form()
# # form.setupUi(window)
# # form.pushButton.clicked.connect(test)
# # window.show()
# # app.exec_()