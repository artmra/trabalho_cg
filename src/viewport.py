from PyQt5.QtGui import QPen
from PyQt5.QtWidgets import QGraphicsView, QMessageBox
from PyQt5.QtCore import Qt, QLineF

from objs import Line, Point, Wireframe, TwoDObj


# Classe que implementa uma viewport para a aplicação
class Viewport(QGraphicsView):

    def __init__(self, world):
        super().__init__()
        self.setFixedSize(800, 800)
        self.dotPen = QPen(Qt.red, 9, Qt.SolidLine, Qt.RoundCap, Qt.MiterJoin)
        self.linePen = QPen(Qt.green, 6, Qt.SolidLine, Qt.FlatCap, Qt.MiterJoin)
        self.wirePen = QPen(Qt.blue, 3, Qt.SolidLine, Qt.FlatCap, Qt.MiterJoin)
        self.setScene(world)

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

    def drawPoint(self, point: Point):
        x, y = self.viewportTransform(point.getX(), point.getY())
        obj = self.scene().addLine(QLineF(x, y, x+1, y+1), self.dotPen)
        self.scene().qGraphicsObjs[point] = [obj]

    def drawLine(self, line: Line):
        x1, y1 = line.getX1_Y1()
        x1, y1 = self.viewportTransform(x1, y1)
        x2, y2 = line.getX2_Y2()
        x2, y2 = self.viewportTransform(x2, y2)
        obj = self.scene().addLine(QLineF(x1, y1, x2, y2), self.linePen)
        self.scene().qGraphicsObjs[line] = [obj]

    def drawWireframe(self, wireframe: Wireframe):
        x1, y1 = wireframe.coords[0]
        x1, y1 = self.viewportTransform(x1, y1)
        x0, y0 = x1, y1
        points = []
        for i in range(1, len(wireframe.coords)):
            x2, y2 = wireframe.coords[i]
            x2, y2 = self.viewportTransform(x2, y2)
            obj = self.scene().addLine(QLineF(x1, y1, x2, y2), self.wirePen)
            points.append(obj)
            x1, y1 = x2, y2
        obj = self.scene().addLine(QLineF(x1, y1, x0, y0), self.wirePen)
        points.append(obj)
        self.scene().qGraphicsObjs[wireframe] = points

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

    def addObj(self, obj: TwoDObj):
        self.scene().objs.append(obj)

    def updateObj(self, obj: TwoDObj):
        self.scene().objs.updateObj(obj)

    def deleteObj(self, objName: str):
        try:
            obj = self.scene().getObj(objName)
            self.scene().deleteObj(obj)
        except:
            msg = QMessageBox()
            msg.setWindowTitle('Não há o que excluir')
            msg.setText(str('A liste de objetos ja sta vazia.'))
            x = msg.exec_()
