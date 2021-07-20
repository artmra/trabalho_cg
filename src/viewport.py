from PyQt5.QtGui import QPen, QPainter, QPalette, QColor
from PyQt5.QtWidgets import QMessageBox, QWidget
from PyQt5.QtCore import Qt

from objs import Line, Point, Wireframe, TwoDObj, TwoDObjType


# Classe que implementa uma viewport para a aplicação
class Viewport(QWidget):

    def __init__(self, world):
        super().__init__()
        self.setFixedSize(800, 800)
        self.world = world
        self.window_ = self.world.getWindow()
        pal = self.palette()
        pal.setColor(QPalette.Background, Qt.black)
        self.setAutoFillBackground(True)
        self.setPalette(pal)
        self.dotPen = QPen(Qt.red, 5, Qt.SolidLine, Qt.RoundCap, Qt.MiterJoin)

    def getViewportCoords(self) -> (float, float, float, float):
        # coords = self.visibleRegion().boundingRect().getCoords()
        # xvpmin = coords[0]
        # yvpmin = coords[1]
        # xvpmax = coords[2]
        # yvpmax = coords[3]
        return self.visibleRegion().boundingRect().getCoords()

    def viewportTransform(self, xw, yw) -> (float, float):
        # aplicar a matriz scn da window as coordenadas do mundo
        xw, yw = self.window_.applySCN(xw, yw)
        # realiza a transformada de viewport
        xwmin, ywmin, xwmax, ywmax = self.window_.getCoords()
        # # aplica a matriz scn ao x/yw min/max
        xwmin, ywmin = self.window_.applySCN(xwmin, ywmin)
        xwmax, ywmax = self.window_.applySCN(xwmax, ywmax)
        xvpmin, yvpmin, xvpmax, yvpmax = self.getViewportCoords()
        return ((xw - xwmin) / (xwmax - xwmin)) * (xvpmax - xvpmin), (1 - ((yw - ywmin) / (ywmax - ywmin))) * (yvpmax - yvpmin)

    def paintEvent(self, event):
        self.drawExys()
        for obj in self.world.objs:
            if obj.twoDType.value == TwoDObjType.POINT.value:
                self.drawPoint(obj)
            elif obj.twoDType.value == TwoDObjType.LINE.value:
                self.drawLine(obj)
            else:
                self.drawWireframe(obj)

    def drawExys(self):
        p1 = QPainter()
        p2 = QPainter()
        p3 = QPainter()
        p4 = QPainter()
        # # painter de 5~8 n sao necessários caso n queira imprimir pontos referentes a cada quadrante
        # p5 = QPainter()
        # p6 = QPainter()
        # p7 = QPainter()
        # p8 = QPainter()
        lenght, height = self.window_.getWindowDimensions()
        center_x, center_y = self.viewportTransform(0,0)
        # coordenadas das retas
        x1_eixo_x, y1_eixo_x = self.viewportTransform((-1) * lenght, 0)
        x2_eixo_x, y2_eixo_x = self.viewportTransform(lenght, 0)
        x1_eixo_y, y1_eixo_y = self.viewportTransform(0, (-1) * height)
        x2_eixo_y, y2_eixo_y = self.viewportTransform(0, height)
        # desenha linha de [0, lenght](direita) no eixo x - red
        p1.begin(self)
        p1.setPen(QColor(150, 0, 0, 127))
        p1.drawLine(center_x, center_y, x2_eixo_x, y2_eixo_x)
        p1.end()
        # desenha linha de [0, -lenght](esquerda) no eixo x - ciano
        p2.begin(self)
        p2.setPen(QColor(0, 150, 150, 127))
        p2.drawLine(center_x, center_y, x1_eixo_x, y1_eixo_x)
        p2.end()
        # desenha linha de [0, height](cima) no eixo y - green
        p3.begin(self)
        p3.setPen(QColor(0, 150, 0, 127))
        p3.drawLine(center_x, center_y, x2_eixo_y, y2_eixo_y)
        p3.end()
        # desenha linha de [0, -height](baixo) no eixo y - pinlk
        p4.begin(self)
        p4.setPen(QColor(150, 0, 150, 127))
        p4.drawLine(center_x, center_y, x1_eixo_y, y1_eixo_y)
        p4.end()
        # # calculos apenas incluidos para pintar pontos em cada um dos quadrantes
        # x1_eixo_x, _ = self.viewportTransform(-50, 0)
        # x2_eixo_x, _ = self.viewportTransform(50, 0)
        # _, y1_eixo_y = self.viewportTransform(0, -50)
        # _, y2_eixo_y = self.viewportTransform(0, 50)
        # # desenhar ponto primeiro quadrante - red
        # p5.begin(self)
        # p5.setPen(QPen(QColor(150, 0, 0, 127), 10, Qt.SolidLine, Qt.FlatCap, Qt.MiterJoin))
        # p5.drawPoint(x2_eixo_x, y2_eixo_y)
        # p5.end()
        # # desenhar ponto segundo quadrante - green
        # p6.begin(self)
        # p6.setPen(QPen(QColor(0, 150, 0, 127), 10, Qt.SolidLine, Qt.FlatCap, Qt.MiterJoin))
        # p6.drawPoint(x1_eixo_x, y2_eixo_y)
        # p6.end()
        # # desenhar ponto terceiro quadrante - blue
        # p7.begin(self)
        # p7.setPen(QPen(QColor(0, 150, 150, 127), 10, Qt.SolidLine, Qt.FlatCap, Qt.MiterJoin))
        # p7.drawPoint(x1_eixo_x, y1_eixo_y)
        # p7.end()
        # # desenhar ponto quarto quadrante - pink
        # p8.begin(self)
        # p8.setPen(QPen(QColor(150, 0, 150, 127), 10, Qt.SolidLine, Qt.FlatCap, Qt.MiterJoin))
        # p8.drawPoint(x2_eixo_x, y1_eixo_y)
        # p8.end()

    def drawPoint(self, point: Point):
        p = QPainter()
        p.begin(self)
        p.setPen(QPen(point.getColor(), 5, Qt.SolidLine, Qt.RoundCap, Qt.MiterJoin))
        x, y = self.viewportTransform(point.getX(), point.getY())
        p.drawPoint(x, y)
        p.end()

    def drawLine(self, line: Line):
        p = QPainter()
        p.begin(self)
        p.setPen(QPen(line.getColor(), 3, Qt.SolidLine, Qt.RoundCap, Qt.MiterJoin))
        x1, y1 = line.getX1_Y1()
        x1, y1 = self.viewportTransform(x1, y1)
        x2, y2 = line.getX2_Y2()
        x2, y2 = self.viewportTransform(x2, y2)
        p.drawLine(x1, y1, x2, y2)
        p.end()

    def drawWireframe(self, wireframe: Wireframe):
        p = QPainter()
        p.begin(self)
        p.setPen(QPen(wireframe.getColor(), 3, Qt.SolidLine, Qt.RoundCap, Qt.MiterJoin))
        x1, y1 = wireframe.coords[0]
        x1, y1 = self.viewportTransform(x1, y1)
        x0, y0 = x1, y1
        for i in range(1, len(wireframe.coords)):
            x2, y2 = wireframe.coords[i]
            x2, y2 = self.viewportTransform(x2, y2)
            p.drawLine(x1, y1, x2, y2)
            x1, y1 = x2, y2
        p.drawLine(x1, y1, x0, y0)
        p.end()

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

    def rotateRight(self):
        self.window_.rotateRight()
        self.update()

    def rotateLeft(self):
        self.window_.rotateLeft()
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
            msg.setText(str('A liste de objetos ja está vazia.'))
            x = msg.exec_()
