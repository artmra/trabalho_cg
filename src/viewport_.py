from PyQt5.QtGui import QPen, QPainter, QColor
from PyQt5.QtWidgets import QGraphicsView, QMessageBox, QWidget
from PyQt5.QtCore import Qt, QLineF

from src.objs import Line, Point, Wireframe, TwoDObj, TwoDObjType

import sys, random


# Classe que implementa uma viewport para a aplicação
from src.window import Window
from world_ import World


class Viewport(QWidget):

    def __init__(self, world):
        super().__init__()
        self.setFixedSize(800, 800)
        self.world = world
        self.window_ = self.world.getWindow()
        self.painter = QPainter()
        self.dotPen = QPen(Qt.red, 9, Qt.SolidLine, Qt.RoundCap, Qt.MiterJoin)
        self.linePen = QPen(Qt.green, 6, Qt.SolidLine, Qt.FlatCap, Qt.MiterJoin)
        self.wirePen = QPen(Qt.blue, 3, Qt.SolidLine, Qt.FlatCap, Qt.MiterJoin)

    def getViewportCoords(self) -> (float, float, float, float):
        # coords = self.visibleRegion().boundingRect().getCoords()
        # xvpmin = coords[0]
        # yvpmin = coords[1]
        # xvpmax = coords[2]
        # yvpmax = coords[3]
        return self.visibleRegion().boundingRect().getCoords()

    def viewportTransform(self, xw, yw) -> (float, float):
        xwmin, ywmin, xwmax, ywmax = self.window_.getCoords()
        xvpmin, yvpmin, xvpmax, yvpmax = self.getViewportCoords()
        return ((float(xw) - xwmin)/(xwmax - xwmin))*(xvpmax - xvpmin), (1 - ((float(yw) - ywmin)/(ywmax - ywmin)))*(yvpmax - yvpmin)


    # atualiza o widget
    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        for obj in self.world.objs:
            if obj.twoDType == TwoDObjType.POINT:
                self.drawPoint(qp, obj)
            elif obj.twoDType == TwoDObjType.LINE:
                self.drawLine(qp, obj)
            else:
                self.drawWireframe(qp, obj)
        qp.end()

    def drawPoint(self, qp: QPainter, point: Point):
        # qp.setPen(self.dotPen)
        x, y = self.viewportTransform(point.getX(), point.getY())
        qp.drawPoint(x, y)
        # obj = self.scene().addLine(QLineF(x, y, x+1, y+1), self.dotPen)
        # self.scene().qGraphicsObjs[point] = [obj]

    def drawLine(self, qp: QPainter, line: Line):
        # qp.setPen(self.linePen)
        x1, y1 = line.getX1_Y1()
        x1, y1 = self.viewportTransform(x1, y1)
        x2, y2 = line.getX2_Y2()
        x2, y2 = self.viewportTransform(x2, y2)
        qp.drawLine(x1, y1, x2, y2)

    def drawWireframe(self, qp: QPainter, wireframe: Wireframe):
        # qp.setPen(self.wirePen)
        x1, y1 = wireframe.coords[0]
        x1, y1 = self.viewportTransform(x1, y1)
        x0, y0 = x1, y1
        # points = []
        for i in range(1, len(wireframe.coords)):
            x2, y2 = wireframe.coords[i]
            x2, y2 = self.viewportTransform(x2, y2)
            qp.drawLine(x1, y1, x2, y2)
            # obj = self.world.addLine(QLineF(x1, y1, x2, y2), self.wirePen)
            # points.append(obj)
            x1, y1 = x2, y2
        qp.drawLine(x1, y1, x0, y0)
        # points.append(obj)
        # self.scene().qGraphicsObjs[wireframe] = points

    def zoomIn(self):
        self.window_.zoomIn()

    def zoomOut(self):
        self.window_.zoomOut()

    def moveUp(self):
        self.window_.moveUp()

    def moveRight(self):
        self.window_.moveRight()

    def moveLeft(self):
        self.moveLeft()

    def moveDown(self):
        self.moveDown()

    def addObj(self, obj: TwoDObj):
        self.world.objs.append(obj)

    # def updateObj(self, obj: TwoDObj):
    #     self.scene().objs.updateObj(obj)

    # def deleteObj(self, objName: str):
    #     try:
    #         obj = self.scene().getObj(objName)
    #         self.scene().deleteObj(obj)
    #     except:
    #         msg = QMessageBox()
    #         msg.setWindowTitle('Não há o que excluir')
    #         msg.setText(str('A liste de objetos ja sta vazia.'))
    #         x = msg.exec_()
