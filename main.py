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

    def __init__(self):
        super(Ui, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setChildrenFocusPolicy(QtCore.Qt.NoFocus)
        # actoins
        self.ui.path_btn.clicked.connect(self.checkPath)
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
        self.ui.path_text.setText(f"path: {self.path} ({self.im_count} photo)")
        if self.im_count > 0:
            self.displayImg()

    def displayImg(self):
        if self.im_count > 0:
            if os.path.isfile(self.image_list[self.image_id]):
                w, h = self.ui.graphicsView.width(), self.ui.graphicsView.height()
                scene = QtWidgets.QGraphicsScene(self)
                pixmap = QPixmap(self.image_list[self.image_id])
                item = QtWidgets.QGraphicsPixmapItem(pixmap.scaled(w, h, QtCore.Qt.KeepAspectRatio))
                scene.addItem(item)
                self.ui.graphicsView.setScene(scene)
                self.ui.info_text.setText(f"image {self.image_id + 1} / {self.im_count}")

    def nextImage(self, order):
        self.image_id += order
        if self.image_id == self.im_count:
            self.image_id = 0
        elif self.image_id < 0:
            self.image_id = self.im_count-1

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_1:
            self.ui.pushButton_1.animateClick()
            self.nextImage(1)
            self.displayImg()
        elif event.key() == QtCore.Qt.Key_2:
            self.ui.pushButton_2.animateClick()
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
            self.ui.pushButton_s.animateClick() 
        else:
            QMainWindow.keyPressEvent(self, event)


app = QApplication([])
ui = Ui()
sys.exit(app.exec_())