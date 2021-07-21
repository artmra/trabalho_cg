from PyQt5.QtGui import QPen, QPainter, QPalette, QColor, QPolygon, QBrush
from PyQt5.QtWidgets import QMessageBox, QWidget
from PyQt5.QtCore import Qt, QPoint

from objs import Line, Point, Wireframe, TwoDObj, TwoDObjType


# Classe que implementa uma viewport para a aplicação
class Viewport(QWidget):

    def __init__(self, world):
        super().__init__()
        self.viewportLenght = 800
        self.viewportHeight = 800
        self.recuoViewport = 30
        self.setFixedSize(self.viewportLenght, self.viewportHeight)
        self.world = world
        self.window_ = self.world.getWindow()
        pal = self.palette()
        pal.setColor(QPalette.Background, QColor(30, 30, 30))
        self.setAutoFillBackground(True)
        self.setPalette(pal)
        self.dotPen = QPen(Qt.red, 5, Qt.SolidLine, Qt.RoundCap, Qt.MiterJoin)

    def getViewportCoords(self) -> (float, float, float, float):
        # coords = self.visibleRegion().boundingRect().getCoords()
        xvpmin = self.recuoViewport - 1 # coordenadas da viewport começam em 0
        yvpmin = self.recuoViewport - 1 # coordenadas da viewport começam em 0
        xvpmax = self.viewportLenght - self.recuoViewport - 1 # coordenadas da viewport começam em 0
        yvpmax = self.viewportHeight - self.recuoViewport - 1 # coordenadas da viewport começam em 0
        return xvpmin, yvpmin, xvpmax, yvpmax

    def viewportTransform(self, xw, yw) -> (float, float):
        # aplicar a matriz scn da window as coordenadas do mundo
        xw, yw = self.window_.applySCN(xw, yw)
        # realiza a transformada de viewport
        xwmin, ywmin, xwmax, ywmax = self.window_.getCoords()
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
        self.drawSubCanvas()

    def drawExys(self):
        p1 = QPainter()
        p2 = QPainter()
        p3 = QPainter()
        p4 = QPainter()
        lenght, height = self.window_.getWindowDimensions()
        x1, y1 = self.viewportTransform(0, 0)
        # desenha linha de [0, lenght](direita) no eixo x - vermelho "claro"
        x2, y2 = self.viewportTransform(lenght, 0)
        line_coords = self.clipingCohenSutherland(x1, y1, x2, y2)
        if line_coords != [0, 0, 0, 0]:
            x1, y1, x2, y2 = line_coords
            p1.begin(self)
            p1.setPen(QPen(QColor(150, 0, 0, 255), 4))
            p1.drawLine(x1, y1, x2, y2)
            p1.end()
        # desenha linha de [0, -lenght](esquerda) no eixo x - vermelho "escuro"
        x2, y2 = self.viewportTransform(-lenght, 0)
        line_coords = self.clipingCohenSutherland(x1, y1, x2, y2)
        if line_coords != [0, 0, 0, 0]:
            x1, x2, x3, x4 = line_coords
            p2.begin(self)
            p2.setPen(QPen(QColor(51, 0, 0, 255), 3))
            p2.drawLine(x1, y1, x2, y2)
            p2.end()
        # desenha linha de [0, height](cima) no eixo y - azul "claro"
        x2, y2 = self.viewportTransform(0, height)
        line_coords = self.clipingCohenSutherland(x1, y1, x2, y2)
        if line_coords != [0, 0, 0, 0]:
            x1, y1, x2, y2 = line_coords
            p3.begin(self)
            p3.setPen(QPen(QColor(0, 0, 150, 255), 4))
            p3.drawLine(x1, y1, x2, y2)
            p3.end()
        # desenha linha de [0, -height](baixo) no eixo y - azul "escuro"
        x2, y2 = self.viewportTransform(0, -height)
        line_coords = self.clipingCohenSutherland(x1, y1, x2, y2)
        if line_coords != [0, 0, 0, 0]:
            x1, y1, x2, y2 = line_coords
            p4.begin(self)
            p4.setPen(QPen(QColor(0, 0, 51, 255), 3))
            p4.drawLine(x1, y1, x2, y2)
            p4.end()

    def drawSubCanvas(self):
        p = QPainter()
        p.begin(self)
        p.setPen(QPen(Qt.white, 3, Qt.SolidLine, Qt.RoundCap, Qt.MiterJoin))
        p.drawLine(self.recuoViewport, self.recuoViewport, self.recuoViewport, self.viewportLenght - self.recuoViewport)
        p.drawLine(self.recuoViewport, self.viewportHeight - self.recuoViewport, self.viewportLenght - self.recuoViewport, self.viewportHeight - self.recuoViewport)
        p.drawLine(self.viewportLenght - self.recuoViewport, self.viewportHeight - self.recuoViewport, self.viewportLenght - self.recuoViewport, self.recuoViewport)
        p.drawLine(self.viewportLenght - self.recuoViewport, self.recuoViewport, self.recuoViewport, self.recuoViewport)
        p.end()

    def drawPoint(self, point: Point):
        p = QPainter()
        p.begin(self)
        p.setPen(QPen(point.getColor(), 5, Qt.SolidLine, Qt.RoundCap, Qt.MiterJoin))
        # aplica o sistema de coordenadas normalizadas
        # todo: deve checar se ponto está dentro da window
        x, y = self.window_.applySCN(point.getX(), point.getY())
        x, y = self.viewportTransform(x, y)
        p.drawPoint(x, y)
        p.end()

    def drawLine(self, line: Line):
        p = QPainter()
        x1, y1 = line.getX1_Y1()
        x1, y1 = self.viewportTransform(x1, y1)
        x2, y2 = line.getX2_Y2()
        x2, y2 = self.viewportTransform(x2, y2)
        line_coords = self.clipingCohenSutherland(x1, y1, x2, y2)
        if line_coords == [0, 0, 0, 0]:
            return
        x1, x2, x3, x4 = line_coords
        p.begin(self)
        p.setPen(QPen(line.getColor(), 3, Qt.SolidLine, Qt.RoundCap, Qt.MiterJoin))
        p.drawLine(x1, y1, x2, y2)
        p.end()

    def drawWireframe(self, wireframe: Wireframe):
        p = QPainter()
        p_ = QPainter()
        p.begin(self)
        p.setPen(QPen(wireframe.getColor(), 3, Qt.SolidLine, Qt.RoundCap, Qt.MiterJoin))
        x1, y1 = wireframe.coords[0]
        x1, y1 = self.viewportTransform(x1, y1)
        x0, y0 = x1, y1
        poly_points = [QPoint(x1, y1)]
        for i in range(1, len(wireframe.coords)):
            x2, y2 = wireframe.coords[i]
            x2, y2 = self.viewportTransform(x2, y2)
            poly_points.append(QPoint(x2, y2))
            p.drawLine(x1, y1, x2, y2)
            x1, y1 = x2, y2
        p.drawLine(x1, y1, x0, y0)
        p.end()
        # preenche o poligono. Talvez tenha q mudar se não der para fazer isso.
        p_.begin(self)
        p_.setBrush(QBrush(wireframe.getColor()))
        p_.drawPolygon(QPolygon(poly_points))
        p_.end()

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

    # retorna o valor inteiro do RC code
    def rcCodeToInt(self, code: list) -> int:
        value = 0
        for i in range(4):
            value = value + (2 ** code[i])
        return value

    # calcula o RC de um ponto qualquer
    def calcRC(self, x: float, y: float,
               xwesq: float, ywtopo: float, xwdir: float, ywfundo: float) -> [int, int, int, int]:
        x1 = 1 if y < ywtopo else 0
        x2 = 1 if y > ywfundo else 0
        x3 = 1 if x > xwdir else 0
        x4 = 1 if x < xwesq else 0
        return [1 if y < ywtopo else 0, # viewport tem eixo y invertido
                1 if y > ywfundo else 0, # viewport tem eixo y invertido
                1 if x > xwdir else 0,
                1 if x < xwesq else 0]

    # Algoritmo Geral para Recorte de Linhas de Cohen-Sutherland. Retorna 0,0,0,0 caso a linha não seja visivel
    # considerando o tamanho atual da viewport; caso contrario retorna as coordenadas em uma lista, ajustadas na
    # ordem x1, y1, x2, y2.
    def clipingCohenSutherland(self, x1: float, y1: float, x2: float, y2: float) -> [float, float, float, float]:
        # xwesq, ywfundo, xwdir, ywtopo = self.getViewportCoords()
        xwesq, ywtopo, xwdir, ywfundo = self.getViewportCoords()
        # Region Codes das linhas
        rc_ini = self.calcRC(x1, y1, xwesq, ywtopo, xwdir, ywfundo)
        rc_fim = self.calcRC(x2, y2, xwesq, ywtopo, xwdir, ywfundo)
        while(1):
            # P1: se 2 RC's forem totalmente zerados, linha totalmente contida e pode desenhar
            if all(rc_ini[i] == 0 for i in range(4)) and rc_ini == rc_fim:
                return x1, y1, x2, y2
            # calcula o and dos 2 cods
            and_result = [1 if rc_ini[i] == 1 and rc_ini[i] == rc_fim[i] else 0 for i in range(4)]
            # checa se o resultado é igual a [0,0,0,0]
            is_zero = all(r == 0 for r in and_result)
            # P2: se o & dos 2 RC's for diferente de zero, está fora da janela e n precisa desenhar
            if not is_zero:
                return 0, 0, 0, 0
            # P3: RCs diferentes e & dos dois igual a 0, parcialmente dentro e valores devem ser ajustados
            if rc_ini != rc_fim and is_zero:
                # pega o maior RC code para ajustar
                rc = rc_ini if self.rcCodeToInt(rc_ini) > self.rcCodeToInt(rc_fim) else rc_fim
                # calcula coeficiente angular
                deltax = x2 - x1
                deltay = y2 - y1
                # futuros valores de x e y para x1 e y1 se RC_==RC_ini ou x2 e y1 caso contrario
                x = 0
                y = 0
                # reta n é vertical ou horizontal
                if deltax != 0 and deltay != 0:
                    m = deltay / deltax
                    # ponto esta no topo
                    if rc[0] == 1:
                        x = x1 + (1 / m) * (ywtopo - y1)
                        y = ywtopo
                    # ponto esta no fundo
                    elif rc[1] == 1:
                        x = x1 + (1 / m) * (ywfundo - y1)
                        y = ywfundo
                    # ponto esta na direita
                    elif rc[2] == 1:
                        y = y1 + m * (xwdir - x1)
                        x = xwdir
                    # ponto esta na esquerda
                    else:
                        y = y1 + m * (xwesq - x1)
                        x = xwesq
                else:
                    # reta perpendicular ao topo da window
                    if rc[0] == 1:
                        x = x1 if rc == rc_ini else x2
                        y = ywtopo
                    # reta perpendicular ao fundo da window
                    elif rc[1] == 1:
                        x = x1 if rc == rc_ini else x2
                        y = ywfundo
                    # reta perpendicular a direita da window
                    elif rc[2] == 1:
                        y = y1 if rc == rc_ini else y2
                        x = xwdir
                    # reta perpendicular a esquerda da window
                    else:
                        y = y1 if rc == rc_ini else y2
                        x = xwesq
                # atualiza o rc e valores de x1 ou x2 e y1 ou y2
                if rc == rc_ini:
                    x1 = x
                    y1 = y
                    rc_ini = self.calcRC(x1, y1, xwesq, ywtopo, xwdir, ywfundo)
                else:
                    x2 = x
                    y2 = y
                    rc_fim = self.calcRC(x2, y2, xwesq, ywtopo, xwdir, ywfundo)