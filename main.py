import os
import sys
from mainUI import Ui_MainWindow
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import math
import cv2
import numpy as np

class MyUI(QMainWindow, Ui_MainWindow):
    signal_delete = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        super(MyUI, self).__init__(parent)
        self.path = ''
        self.index = 0
        self.list = []
        self.setupUi(self)
        self.btnOpen.clicked.connect(self.btnOpen_clicked)
        self.btnLast.clicked.connect(self.btnLast_clicked)
        self.btnNext.clicked.connect(self.btnNext_clicked)
        self.btnDelete.clicked.connect(self.btnDelete_clicked)
        self.btnSave.clicked.connect(self.btnSave_clicked)
        self.imageBox_Mouse.signal_refresh_list.connect(self.refresh_list)
        self.signal_delete.connect(self.imageBox_Mouse.deleteAt)
        if not os.path.exists('last_index.txt'):
            f = open('last_index.txt', 'w')
            f.write('\n')
            f.write('0')
            f.close()



    def btnOpen_clicked(self):
        self.path = QFileDialog.getExistingDirectory()
        if len(self.path) > 0:
            self.list = os.listdir(self.path)
            f = open('last_index.txt', 'r')
            old_dir = f.readline()
            if old_dir[0:-1] == self.path:
                self.index = int(f.readline())
                print(self.index)
            else:
                self.index = 0
            f.close()
            if self.index >= len(self.list):
                self.index = 0
            self.open_image()

    def btnLast_clicked(self):
        if self.index > 0:
            self.index = self.index - 1
            self.open_image()
            self.clearList()
            self.imageBox_Mouse.clearAll()

    def btnNext_clicked(self):
        if self.index < len(self.list) - 1:
            self.index = self.index + 1
            self.open_image()
            self.clearList()
            self.imageBox_Mouse.clearAll()


    def open_image(self):
        p = self.path + '/' + self.list[self.index]
        img = QPixmap(p)
        img = img.scaled(self.imageBox.size(), Qt.KeepAspectRatio)
        self.imageBox.setPixmap(img)

    def refresh_list(self, a):
        self.listWidget.addItem(str(a-1))

    def btnDelete_clicked(self):
        num = self.listWidget.currentIndex().data()
        if num is not None:
            sum = self.listWidget.count()
            self.listWidget.takeItem(sum - 1)
            self.signal_delete.emit(int(num))

    def clearList(self):
        sum = self.listWidget.count()
        for i in range(sum):
            self.listWidget.takeItem(0)

    def btnSave_clicked(self):
        if self.path is not [] and self.imageBox_Mouse.wires is not []:
            marks = []
            img = cv2.imread(self.path + '/' + self.list[self.index], 0)
            name = self.list[self.index][0:self.list[self.index].rfind('.')]
            dir_YOLO = self.path[0:self.path.rfind('/')] + '/marks_YOLO'
            dir_crop = self.path[0:self.path.rfind('/')] + '/crops'
            dir_wires = self.path[0:self.path.rfind('/')] + '/wires'
            dir_seg = self.path[0:self.path.rfind('/')] + '/segmentation'
            k = img.shape[1] / self.imageBox_Mouse.width()
            if not os.path.exists(dir_YOLO):
                os.makedirs(dir_YOLO)
            if not os.path.exists(dir_crop):
                os.makedirs(dir_crop)
            if not os.path.exists(dir_wires):
                os.makedirs(dir_wires)
            if not os.path.exists(dir_seg):
                os.makedirs(dir_seg)
            f = open('last_index.txt', 'w')
            f.write(self.path)
            f.write('\r')
            f.write(str(self.index))
            f.close()
            for idx, wire in enumerate(self.imageBox_Mouse.wires):
                m = [0]
                x_min = self.imageBox_Mouse.size().width()
                y_min = self.imageBox_Mouse.size().height()
                x_max = 0
                y_max = 0
                for point in wire:
                    if point.x() < x_min:
                        x_min = point.x()
                    if point.x() > x_max:
                        x_max = point.x()
                    if point.y() < y_min:
                        y_min = point.y()
                    if point.y() > y_max:
                        y_max = point.y()
                bolder = 20
                x_min = max(x_min - bolder, 0)
                x_max = min(x_max + bolder, self.imageBox.size().width())
                y_min = max(y_min - bolder, 0)
                y_max = min(y_max + bolder, self.imageBox.size().height())
                middle_x = (x_min + x_max) / 2
                middle_y = (y_min + y_max) / 2
                m.append(middle_x / self.imageBox.size().width())
                m.append(middle_y / self.imageBox.size().height())
                m.append((x_max - x_min) / self.imageBox.size().width())
                m.append((y_max - y_min) / self.imageBox.size().height())
                marks.append(m)
                crop_img = img[int(img.shape[0]*(m[2]-m[4]/2)):math.ceil(img.shape[0]*(m[2]+m[4]/2)),
                            int(img.shape[1]*(m[1]-m[3]/2)): math.ceil(img.shape[1]*(m[1]+m[3]/2))]
                self.save_crop(crop_img, dir_crop + '/' + name + '_' + '%02d'%idx + '.jpg')
                adjust_wire = []
                offset = (int(img.shape[1]*(m[1]-m[3]/2)), int(img.shape[0]*(m[2]-m[4]/2)))
                for w in wire:
                    adjust_wire.append(QPointF(w.x()*k-offset[0], w.y()*k-offset[1]))
                self.save_segmentation(adjust_wire, crop_img.shape, dir_seg + '/' + name, '%02d' % idx + '.jpg')

        self.save_wires(dir_wires + '/' + name + '.txt')
        self.save_YOLO(marks, dir_YOLO + '/' + name + '.txt')

    def save_YOLO(self, marks, txt_name):
        f = open(txt_name, 'w')
        for m in marks:
            for num in m:
                f.write(str(round(num, 6)))
                f.write(' ')
            f.write('\n')

    def save_crop(self, crop_img, crop_name):
        min_pix = 255
        max_pix = 0
        for i in range(crop_img.shape[0]):
            for j in range(crop_img.shape[1]):
                if crop_img[i, j] < min_pix:
                    min_pix = crop_img[i, j]
                if crop_img[i, j] > max_pix:
                    max_pix = crop_img[i, j]
        for i in range(crop_img.shape[0]):
            for j in range(crop_img.shape[1]):
                crop_img[i, j] = int((crop_img[i, j] - min_pix) / (max_pix - min_pix) * 255)
        cv2.imwrite(crop_name, crop_img)

    def save_wires(self, dir_wires):
        f = open(dir_wires, 'w')
        for w in self.imageBox_Mouse.wires:
            f.write('0 ')
            for p in w:
                f.write(str(round(p.x() / self.imageBox_Mouse.width(), 6)))
                f.write(' ')
                f.write(str(round(p.y() / self.imageBox_Mouse.height(), 6)))
                f.write(' ')
            f.write('\n')
        f.close()

    def save_segmentation(self, w, shape, dir_seg, app):
        img_w = np.zeros(shape, np.uint8)
        img_p = np.zeros(shape, np.uint8)
        for i in range(shape[0]):
            for j in range(shape[1]):
                if self.near_wire(QPoint(j, i), w):
                    img_w[i, j] = 255
                if self.near_points(QPoint(j, i), w):
                    img_p[i, j] = 255
        cv2.imwrite(dir_seg+'_0_'+app, img_w)
        cv2.imwrite(dir_seg+'_1_'+app, img_p)

    def near_points(self, p, wire):
        for p1 in wire:
            if math.sqrt((p1.x()-p.x())**2+(p1.y()-p.y())**2) <= 5:
                return True
        return False


    def near_wire(self, p, w):
        for i in range(len(w)-1):
            if self.near_line(p, w[i], w[i+1]):
                return True
        return False

    def near_line(self, p, p1, p2):
        vec0 = (p2.x() - p1.x(), p2.y() - p1.y())
        vec1 = (p.x() - p1.x(), p.y() - p1.y())
        vec2 = (p.x() - p2.x(), p.y() - p2.y())
        a = math.sqrt(vec0[0]**2 + vec0[1]**2)
        b = math.sqrt(vec1[0]**2 + vec1[1]**2)
        c = math.sqrt(vec2[0]**2 + vec2[1]**2)
        if b < 5 or c < 5:
            return True
        if vec1[0]*vec0[0] + vec1[1]*vec0[1] < 0:
            return False
        if vec2[0]*vec0[0] + vec2[1]*vec0[1] > 0:
            return False
        p = (a+b+c)/2
        q = p*(p-a)*(p-b)*(p-c)
        if q < 0:
            return True
        s = math.sqrt(p*(p-a)*(p-b)*(p-c))
        if s > a*5/2:
            return False
        return True


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MyUI()
    mainWindow.show()
    sys.exit(app.exec_())