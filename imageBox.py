from PyQt5 import QtCore, QtWidgets
from PyQt5.Qt import *
from PyQt5.QtCore import *

class imageBox(QtWidgets.QLabel):
    signal_refresh_list = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        super(imageBox, self).__init__(parent)
        self.points = []
        self.wires = []
        self.currentPoint = QPoint(0, 0)
        self.anchorPoint = QPoint(-1, -1)
        self.setCursor(Qt.CrossCursor)
        self.setMouseTracking(True)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.contextMenu = QMenu(self)
        self.customContextMenuRequested.connect(self.showMenu)
        self.reselectLast = self.contextMenu.addAction('Reselect last')
        self.abandon = self.contextMenu.addAction('Abandon')
        self.apply = self.contextMenu.addAction('Apply')
        self.reselectLast.triggered.connect(self.reselectLastMenu_triggered)
        self.abandon.triggered.connect(self.abandonMenu_triggered)
        self.apply.triggered.connect(self.applyMenu_triggered)

    def showMenu(self):
        self.contextMenu.exec_(QCursor.pos())

    def reselectLastMenu_triggered(self):
        if len(self.points) > 1:
            self.points.pop(-1)
            self.anchorPoint = self.points[len(self.points) - 1]
            self.update()
        elif len(self.points) == 1:
            self.points = []
            self.anchorPoint = QPoint(-1, -1)
            self.update()

    def abandonMenu_triggered(self):
        self.points = []
        self.anchorPoint = QPoint(-1, -1)
        self.update()

    def applyMenu_triggered(self):
        if len(self.points) >= 2:
            self.wires.append(self.points)
            self.points = []
            self.anchorPoint = QPoint(-1, -1)
            self.update()
            self.signal_refresh_list.emit(len(self.wires))

    def mouseMoveEvent(self, QMouseEvent):
        self.currentPoint = QMouseEvent.pos()
        self.update()


    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.buttons() == QtCore.Qt.LeftButton:
            self.anchorPoint = QMouseEvent.pos()
            self.points.append(self.anchorPoint)
            self.update()

    def paintEvent(self, QPaintEvent):
        p = QPainter(self)
        p.setPen(QPen(Qt.red, 2, Qt.SolidLine))
        font = QFont('宋体', 16, QFont.Bold, True)
        p.setFont(font)
        for idx, w in enumerate(self.wires):
            p.drawPolyline(self.convert2polygon(w))
            p.drawText(w[0].x(), w[0].y(), str(idx))
        if len(self.points) > 1:
            p.drawPolyline(self.convert2polygon(self.points))
        if self.anchorPoint.x() >= 0 and self.anchorPoint.y() >= 0:
            p.drawLine(self.anchorPoint.x(), self.anchorPoint.y(), self.currentPoint.x(), self.currentPoint.y())

    def convert2polygon(self, points):
        return QPolygon(points)

    def deleteAt(self, index):
        self.wires.pop(index)
        self.update()

    def clearAll(self):
        self.points = []
        self.wires = []
        self.currentPoint = QPoint(0, 0)
        self.anchorPoint = QPoint(-1, -1)
        self.update()
