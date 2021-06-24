from PyQt5.QtGui import QPen, QPainter
from PyQt5.QtWidgets import QGraphicsView, QGraphicsItem
from PyQt5.QtCore import Qt, QLineF
import random

from src.objs import Line, Point, Wireframe
from world import World


# Classe que implementa uma viewport para a aplicação
class Viewport(QGraphicsView):

    def __init__(self, world):
        super().__init__()
        self.setFixedSize(800, 800)
        self.pen = QPen(Qt.red, 3, Qt.SolidLine, Qt.FlatCap, Qt.MiterJoin)
        self.setScene(world)
        # xv1, yv1 = self.viewportTransform(0, 400)
        # xv2, yv2 = self.viewportTransform(0, -400)
        # xh1, yh1 = self.viewportTransform(400, 0)
        # xh2, yh2 = self.viewportTransform(-400, 0)
        # self.scene().addLine(QLineF(xv1, yv1, xv2, yv2), QPen(Qt.gray, 5, Qt.SolidLine, Qt.FlatCap, Qt.MiterJoin))
        # self.scene().addLine(QLineF(xh1, yh1, xh2, yh2), QPen(Qt.gray, 5, Qt.SolidLine, Qt.FlatCap, Qt.MiterJoin))

    def getViewportCoords(self) -> (float, float, float, float):
        # coords = self.visibleRegion().boundingRect().getCoords()
        # xvpmin = coords[0]
        # yvpmin = coords[1]
        # xvpmax = coords[2]
        # yvpmax = coords[3]
        return self.visibleRegion().boundingRect().getCoords()

    def viewportTransform(self, xw, yw) -> (float, float):
        xwmin, ywmin, xwmax, ywmax = self.scene().getWorlCoords()
        xvpmin, yvpmin, xvpmax, yvpmax = self.getViewportCoords()
        return ((float(xw) - xwmin)/(xwmax - xwmin))*(xvpmax - xvpmin), (1 - ((float(yw) - ywmin)/(ywmax - ywmin)))*(yvpmax - yvpmin)

    def drawLine(self, line: Line):
        x1, y1 = line.getX1_Y1()
        x1, y1 = self.viewportTransform(x1, y1)
        x2, y2 = line.getX2_Y2()
        x2, y2 = self.viewportTransform(x2, y2)
        self.scene().addLine(QLineF(x1, y1, x2, y2), self.pen)

    def drawPoint(self, point: Point):
        x, y = self.viewportTransform(point.getX(), point.getY())
        self.scene().addLine(QLineF(x, y, x, y+1), self.pen)

    def drawWireframe(self, wireframe: Wireframe):
        x1, y1 = wireframe.coords[0]
        x1, y1 = self.viewportTransform(x1, y1)
        x0, y0 = x1, y1
        for i in range(1, len(wireframe.coords)):
            x2, y2 = wireframe.coords[i]
            x2, y2 = self.viewportTransform(x2, y2)
            self.scene().addLine(QLineF(x1, y1, x2, y2), self.pen)
            x1, y1 = x2, y2
        self.scene().addLine(QLineF(x1, y1, x0, y0), self.pen)




    def zoomIn(self):
        self.scale(1.2, 1.2)

    def zoomOut(self):
        self.scale(1/1.2, 1/1.2)

    def moveUp(self):
        scrollBar = self.verticalScrollBar()
        scrollBar.setValue(scrollBar.value() - 20)

    def moveRight(self):
        scrollBar = self.horizontalScrollBar()
        scrollBar.setValue(scrollBar.value() + 20)

    def moveLeft(self):
        scrollBar = self.horizontalScrollBar()
        scrollBar.setValue(scrollBar.value() - 20)

    def moveDown(self):
        scrollBar = self.verticalScrollBar()
        scrollBar.setValue(scrollBar.value() + 20)

    def addObj(self, obj: object) -> object:
        self.scene().objs.append(obj)

    def updateObj(self, obj):
        self.scene().objs.updateObj(obj)

    def deleteObj(self, obj):
        self.scene().objs.remove(obj)
        # self.scene().objs.deleteObj(obj)
