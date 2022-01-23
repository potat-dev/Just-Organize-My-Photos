from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QFileDialog
import os, sys, glob, math, subprocess
from math import floor, log, pow
from PyQt5.QtGui import QPixmap
from datetime import datetime
from PyQt5 import QtCore
from PIL import Image
from ui import *

def convert_size(size_bytes):
   if size_bytes == 0: return "0"
   i = int(floor(log(size_bytes, 1024)))
   s = round(size_bytes / pow(1024, i), 2)
   return f"{s} {('B','KB','MB','GB')[i]}"

def getModifyDate(path):
    ts = os.path.getmtime(path)
    return "Null" if ts < 0 else datetime.fromtimestamp(ts).strftime('%d.%m.%Y')

class Ui(QMainWindow):
    #TODO: вынести код в удобные красивые функции
    #TODO: реализовать алгоритм выбора папки для шортката (в процессе)

    def __init__(self):
        # variables
        self.image_id   = 0
        self.im_count   = 0
        self.image_list = []
        self.path       = ""
        self.image_path = ""
        self.image      = None
        self.scene      = None
        self.folders    = {}
        
        super(Ui, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setChildrenFocusPolicy(QtCore.Qt.NoFocus)
        self.ui.path_btn.clicked.connect(self.checkPath)
        self.ui.btn_next.clicked.connect(self.nextImage)
        self.ui.btn_prev.clicked.connect(self.prevImage)
        self.ui.btn_del.clicked.connect(self.deleteImage)
        self.ui.graphicsView.setMouseTracking(True)
        self.ui.graphicsView.viewport().installEventFilter(self)

        self.ui.path_btn.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.path_btn.customContextMenuRequested.connect(self.handle_right_click)
        self.show()

    def handle_right_click(self):
        print("жопа")
    
    def nextImage(self): self.changeImage(1)
    def prevImage(self): self.changeImage(-1)

    def viewImage(self):
        if self.image_path != "":
            os.startfile(self.image_path, 'open')

    def showImageInExplorer(self):
        if self.image_path != "":
            subprocess.run([
                os.path.join(os.getenv('WINDIR'), 'explorer.exe'),
                '/select,',
                os.path.normpath(self.image_path)])

    def setChildrenFocusPolicy(self, policy):
        def recursiveSetChildFocusPolicy (parentQWidget):
            for childQWidget in parentQWidget.findChildren(QtWidgets.QWidget):
                childQWidget.setFocusPolicy(policy)
                recursiveSetChildFocusPolicy(childQWidget)
        recursiveSetChildFocusPolicy(self.ui.centralwidget)

    def pickDirectory(self):
        return str(QFileDialog.getExistingDirectory(self, "Select Directory"))
    
    def checkPath(self): #! currently not supporting RAW, ARW, ...
        temp = self.pickDirectory()
        if temp != "":
            self.path = temp
            self.image_list = [item.replace("\\", "/") for i in [glob.glob(f"{self.path}/*{ext}") for ext in ["jpg","jpeg","png"]] for item in i]
            self.im_count = len(self.image_list)
            self.image_id = 0
            self.ui.path_text.setText(f"path: {self.path} ({self.im_count} photo)")
            if self.im_count > 0:
                self.displayImg()
    
    def deleteImage(self):
        if self.im_count > 0:
            del_img = self.image_list.pop(self.image_id)
            self.image.close()
            QtCore.QFile.moveToTrash(del_img)
            self.im_count = len(self.image_list)
            if self.image_id == self.im_count: self.image_id -= 1
            if self.im_count > 0: self.displayImg()
            else: self.clearPreview()
    
    def clearPreview(self):
        self.scene.clear()
        self.ui.graphicsView.viewport().update()
        self.ui.path_text.setText(f"File: Null\nPath: {self.path}")
        self.ui.info_text.setText(
                        f"Image {self.image_id + 1} / {self.im_count}\n" +
                        "[ all files sorted ]")

    def displayImg(self):
        if self.im_count > 0:
            self.image_path = self.image_list[self.image_id]
            if os.path.isfile(self.image_path):
                w, h = self.ui.graphicsView.width(), self.ui.graphicsView.height()
                self.scene = QtWidgets.QGraphicsScene(self)
                pixmap = QPixmap(self.image_path)
                item = QtWidgets.QGraphicsPixmapItem(pixmap.scaled(w, h, QtCore.Qt.KeepAspectRatio))
                self.scene.addItem(item)
                self.ui.graphicsView.setScene(self.scene)
                self.ui.path_text.setText(f"File: {os.path.basename(self.image_path)}\nPath: {self.path}")
                
                try:
                    self.image = Image.open(self.image_path)
                    self.ui.info_text.setText(
                        f"Image {self.image_id + 1} / {self.im_count}\n" +
                        f"Res: {' × '.join([str(i) for i in self.image.size])}\n" +
                        f"Size: {convert_size(os.path.getsize(self.image_path))}\n" +
                        f"Date: {getModifyDate(self.image_path)}") # full: %d.%m.%Y %H:%M:%S
                except OSError:
                    print("что-то пошло по пизде") # debug
                    self.ui.info_text.setText(
                        f"Image {self.image_id + 1} / {self.im_count}\nRes: Null\n" +
                        f"Size: {convert_size(os.path.getsize(self.image_path))}\nDate: Null\n" +
                        "[ corrupted image file ]")

    # def mousePressEvent(self, event):
    #     if event.button() == QtCore.Qt.LeftButton:
    #         print("Press!")

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.MouseButtonPress:
            if event.button() == QtCore.Qt.LeftButton:
                self.viewImage()
            elif event.button() == QtCore.Qt.RightButton:
                self.showImageInExplorer()
        return super(Ui, self).eventFilter(source, event)

    def changeImage(self, order):
        self.image_id += order
        if self.image_id == self.im_count:
            self.image_id = 0
        elif self.image_id < 0:
            self.image_id = self.im_count-1
        self.displayImg()

    #? beta
    def move2folder(self, folder):
        #* должно быть похоже на функцию удаления
        #* нужно закрывать файл перед перемещением
        if folder not in self.folders.keys() \
        or QtWidgets.QApplication.keyboardModifiers() == QtCore.Qt.ControlModifier:
            self.folders |= {str(folder):"None"}
            print("выбрать папку и добавить новый ключ", folder)
        # сделать проверку, выбрал ли пользователь папку
        if folder in self.folders.keys():
            print("тупо переместить файл в папку", folder)

    def keyPressEvent(self, event):
        k = event.key()
        if k == QtCore.Qt.Key_Delete:  self.deleteImage()
        elif k == QtCore.Qt.Key_Right: self.changeImage(1)
        elif k == QtCore.Qt.Key_Left:  self.changeImage(-1)

        elif k == QtCore.Qt.Key_1: self.move2folder("1") #? test
        elif k == QtCore.Qt.Key_2: self.move2folder("2")
        elif k == QtCore.Qt.Key_3: self.move2folder("3")
        elif k == QtCore.Qt.Key_4: self.move2folder("4")
        elif k == QtCore.Qt.Key_5: self.move2folder("5")
        elif k == QtCore.Qt.Key_6: pass
        elif k == QtCore.Qt.Key_7: pass
        elif k == QtCore.Qt.Key_8: pass
        elif k == QtCore.Qt.Key_9: pass
        elif k == QtCore.Qt.Key_0: pass

        elif k == QtCore.Qt.Key_Enter: pass
        elif k == QtCore.Qt.Key_Space: pass

        else: QMainWindow.keyPressEvent(self, event)


app, ui = QApplication([]), Ui()
sys.exit(app.exec_()) #* run app