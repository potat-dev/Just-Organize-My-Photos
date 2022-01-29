from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QFileDialog
import os, sys, glob, math, subprocess
from math import floor, log, pow
from PyQt5.QtGui import QPixmap
from datetime import datetime
from functools import partial
from PyQt5.QtCore import Qt
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
    def __init__(self):
        super(Ui, self).__init__()

        self.image_list, self.folders = [], {}
        self.image_id, self.img_count = 0, 0
        self.image, self.scene = None, None
        self.path, self.image_path = "", ""

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()

        self.setChildrenFocusPolicy(QtCore.Qt.NoFocus)
        self.ui.path_btn.clicked.connect(self.selectFolder)
        self.ui.btn_next.clicked.connect(self.nextImage)
        self.ui.btn_prev.clicked.connect(self.prevImage)
        self.ui.btn_del.clicked.connect(self.deleteImage)
        self.ui.canvas.setMouseTracking(True)
        self.ui.canvas.viewport().installEventFilter(self)

        # настраиваем драгндроп
        self.ui.canvas.dropEvent = lambda e: self.open_dnd(e)
        self.ui.canvas.dragEnterEvent = lambda e: e.accept() if e.mimeData().hasUrls() else e.ignore()
        self.ui.canvas.dragMoveEvent  = lambda e: e.accept() if e.mimeData().hasUrls() else e.ignore()

        self.tags = [str(i) for i in range(1, 10)] + ["0", "Enter", "Space"]
        self.keys = [Qt.Key_1, Qt.Key_2, Qt.Key_3, Qt.Key_4, Qt.Key_5,
                     Qt.Key_6, Qt.Key_7, Qt.Key_8, Qt.Key_9, Qt.Key_0,
                     Qt.Key_Enter, Qt.Key_Space]

        self.buttons = [self.ui.bt1, self.ui.bt2, self.ui.bt3, self.ui.bt4,
                        self.ui.bt5, self.ui.bt6, self.ui.bt7, self.ui.bt8,
                        self.ui.bt9, self.ui.bt0, self.ui.btE, self.ui.btS]

        for btn, tag in zip(self.buttons, self.tags):
            btn.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
            btn.clicked.connect(partial(self.move2folder, folder=tag))
            btn.customContextMenuRequested.connect(partial(self.move2folder, folder=tag, change=True))

    def handle_right_click(self): print("test")
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

    def selectFolder(self): self.checkPath(self.pickDirectory())
    def pickDirectory(self): return str(QFileDialog.getExistingDirectory(self, "Select Directory"))

    def open_dnd(self, e):
        if e.mimeData().hasUrls():
            #TODO: сделать сортировку сразу нескольких папок
            path = e.mimeData().urls()[0].toLocalFile() #? берем только первую папку
            if os.path.isdir(path):
                self.checkPath(path)
    
    def checkPath(self, folder):
        if folder == "": return None
        self.path = folder
        self.image_list = [
            item.replace("\\", "/") for i in [
                glob.glob(f"{self.path}/*{ext}") for ext in ["jpg","jpeg","png"]
            ] for item in i
        ]
        self.img_count, self.image_id = len(self.image_list), 0
        self.ui.path_text.setText(f"path: {self.path} ({self.img_count} photo)")
        if self.img_count > 0:
            self.displayImg()
    
    def deleteImage(self):
        if self.img_count > 0:
            del_img = self.image_list.pop(self.image_id)
            self.img_count = len(self.image_list)
            if self.image_id == self.img_count: self.image_id -= 1
            if self.img_count > 0: self.displayImg()
            else: self.clearPreview()
            self.image.close()
            if QtWidgets.QApplication.keyboardModifiers() == Qt.ControlModifier:
                os.remove(del_img)
            else:
                QtCore.QFile.moveToTrash(del_img)
    
    def clearPreview(self):
        self.scene.clear()
        self.ui.canvas.viewport().update()
        self.ui.path_text.setText(f"File: Null\nPath: {self.path}")
        self.ui.info_text.setText(
            f"Image {self.image_id + 1} / {self.img_count}\n" +
            "[ all files sorted ]")

    def displayImg(self):
        if self.img_count <= 0: return None
        self.image_path = self.image_list[self.image_id]
        if os.path.isfile(self.image_path):
            w, h = self.ui.canvas.width(), self.ui.canvas.height()
            self.scene = QtWidgets.QGraphicsScene(self)
            pixmap = QPixmap(self.image_path)
            item = QtWidgets.QGraphicsPixmapItem(pixmap.scaled(w, h, QtCore.Qt.KeepAspectRatio))
            self.scene.addItem(item)
            self.ui.canvas.setScene(self.scene)
            self.ui.path_text.setText(f"File: {os.path.basename(self.image_path)}\nPath: {self.path}")
            try:
                self.image = Image.open(self.image_path)
                self.ui.info_text.setText(
                    f"Image {self.image_id + 1} / {self.img_count}\n" +
                    f"Res: {' × '.join([str(i) for i in self.image.size])}\n" +
                    f"Size: {convert_size(os.path.getsize(self.image_path))}\n" +
                    f"Date: {getModifyDate(self.image_path)}") # full: %d.%m.%Y %H:%M:%S
            except OSError:
                self.ui.info_text.setText(
                    f"Image {self.image_id + 1} / {self.img_count}\nRes: Null\n" +
                    f"Size: {convert_size(os.path.getsize(self.image_path))}\nDate: Null\n" +
                    "[ corrupted image file ]")

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.MouseButtonPress:
            if event.button() == QtCore.Qt.LeftButton:
                self.viewImage()
            elif event.button() == QtCore.Qt.RightButton:
                self.showImageInExplorer()
        return super(Ui, self).eventFilter(source, event)

    def changeImage(self, order):
        self.image_id += order
        if self.image_id == self.img_count:
            self.image_id = 0
        elif self.image_id < 0:
            self.image_id = self.img_count-1
        self.displayImg()

    def move2folder(self, folder, change=False):
        if self.img_count <= 0: return None
        modifier = QtWidgets.QApplication.keyboardModifiers()
        if change or folder not in self.folders.keys() \
        or modifier in (Qt.ControlModifier, Qt.ShiftModifier):
            path = self.pickDirectory()
            if path == "" : return None
            self.folders |= {folder: path}
            self.buttons[self.tags.index(folder)].setText(folder + "\n" + os.path.basename(path))

        if folder in self.folders.keys():
            self.image.close() # нужно закрывать файл перед перемещением
            img_pth = self.image_list.pop(self.image_id)
            os.replace(img_pth, os.path.join(self.folders[folder], os.path.basename(img_pth)))
            self.img_count = len(self.image_list)
            if self.image_id == self.img_count: self.image_id -= 1
            if self.img_count > 0: self.displayImg()
            else: self.clearPreview()

    def keyPressEvent(self, event):
        k = event.key()
        if k == QtCore.Qt.Key_Delete:  self.deleteImage()
        elif k == QtCore.Qt.Key_Right: self.changeImage(1)
        elif k == QtCore.Qt.Key_Left:  self.changeImage(-1)
        elif k in self.keys: self.move2folder(self.tags[self.keys.index(k)])
        else: QMainWindow.keyPressEvent(self, event)


app, ui = QApplication([]), Ui()
sys.exit(app.exec_())