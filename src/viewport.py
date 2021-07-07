from PyQt5.QtGui import QPen, QPainter
from PyQt5.QtWidgets import QMessageBox, QWidget
from PyQt5.QtCore import Qt

from src.objs import Line, Point, Wireframe, TwoDObj, TwoDObjType

# Classe que implementa uma viewport para a aplicação
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
        x, y = self.viewportTransform(point.getX(), point.getY())
        qp.drawPoint(x, y)

    def drawLine(self, qp: QPainter, line: Line):
        x1, y1 = line.getX1_Y1()
        x1, y1 = self.viewportTransform(x1, y1)
        x2, y2 = line.getX2_Y2()
        x2, y2 = self.viewportTransform(x2, y2)
        qp.drawLine(x1, y1, x2, y2)

    def drawWireframe(self, qp: QPainter, wireframe: Wireframe):
        x1, y1 = wireframe.coords[0]
        x1, y1 = self.viewportTransform(x1, y1)
        x0, y0 = x1, y1
        for i in range(1, len(wireframe.coords)):
            x2, y2 = wireframe.coords[i]
            x2, y2 = self.viewportTransform(x2, y2)
            qp.drawLine(x1, y1, x2, y2)
            x1, y1 = x2, y2
        qp.drawLine(x1, y1, x0, y0)

    def zoomIn(self):
        self.window_.zoomIn()
        self.update()

    def zoomOut(self):
        self.window_.zoomOut()
        self.update()

    def moveUp(self):
        self.window_.moveUp()
        self.update()

    def moveRight(self):
        self.window_.moveRight()
        self.update()

    def moveLeft(self):
        self.window_.moveLeft()
        self.update()

    def moveDown(self):
        self.window_.moveDown()
        self.update()

    def addObj(self, obj: TwoDObj):
        self.world.objs.append(obj)
        self.update()

    def updateObj(self, obj: TwoDObj):
        self.world.updateObj(obj)

    def deleteObj(self, objName: str):
        try:
            self.world.deleteObj(self.world.getObj(objName))
            self.update()
        except:
            msg = QMessageBox()
            msg.setWindowTitle('Não há o que excluir')
            msg.setText(str('A liste de objetos ja sta vazia.'))
            x = msg.exec_()
