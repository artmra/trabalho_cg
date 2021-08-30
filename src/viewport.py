from PyQt5.QtGui import QPen, QPainter, QPalette, QColor, QPolygon, QBrush
from PyQt5.QtWidgets import QMessageBox, QWidget
from PyQt5.QtCore import Qt, QPoint

from objs import Line, Point, Wireframe, BezierCurve, TwoDObj, TwoDObjType


# Classe que implementa uma viewport para a aplicação
class Viewport(QWidget):

    def __init__(self, world):
        super().__init__()
        self.viewportLenght = 800
        self.viewportHeight = 800
        self.recuoViewport = 30
        self.setFixedSize(self.viewportLenght, self.viewportHeight)
        self.world = world
        pal = self.palette()
        pal.setColor(QPalette.Background, QColor(255, 255, 255))
        self.setAutoFillBackground(True)
        self.setPalette(pal)
        self.dotPen = QPen(Qt.red, 5, Qt.SolidLine, Qt.RoundCap, Qt.MiterJoin)
        self.clippingAlg = 0
        # test objs
        self.addObj(Wireframe('test_wireframe', [(10, 10), (60, 100), (110, 20), (160, 100), (210, 10)]))
        self.addObj(Line('test_line_1', [(0, 0), (-100, -100)], (0, 200, 0)))
        self.addObj(Line('test_line_2', [(0, 0), (100, 100)], (0, 100, 0)))
        self.addObj(Point('test_point_1', (-50, -50)))
        self.addObj(Point('test_point_2', (-35, 10)))
        self.addObj(Point('test_point_3', (79, -58)))
        self.addObj(BezierCurve('test_bezier_curve', [(0, 0), (0, 100), (100, 100), (100, 0)]))

    # retorna os valores xy_vpmin e xy_vpmax
    def getViewportCoords(self) -> (float, float, float, float):
        xvpmin = self.recuoViewport
        yvpmin = self.recuoViewport
        xvpmax = self.viewportLenght - self.recuoViewport
        yvpmax = self.viewportHeight - self.recuoViewport
        return xvpmin, yvpmin, xvpmax, yvpmax

    # realiza a transformada de viewport para um ponto qualquer; os valores passados para esse método já são considera-
    # dos os valores clipados e normalizados dos objetos.
    def viewportTransform(self, xw, yw) -> (float, float):
        # realiza a transformada de viewport
        # xwmin, ywmin, xwmax, ywmax = self.world.getWindow().getCoords()
        xwmin, ywmin = -1, -1
        xwmax, ywmax = 1, 1
        xvpmin, yvpmin, xvpmax, yvpmax = self.getViewportCoords()
        return ((xw - xwmin) / (xwmax - xwmin)) * (xvpmax - xvpmin) + xvpmin,\
               (1 - ((yw - ywmin) / (ywmax - ywmin))) * (yvpmax - yvpmin) + yvpmin

    # método que é chamado toda vez que a viewport é atualizada via chamda de .update()
    def paintEvent(self, event):
        self.drawExys()
        for obj in self.world.objs:
            if obj.twoDType.value == TwoDObjType.POINT.value:
                self.drawPoint(obj)
            elif obj.twoDType.value == TwoDObjType.LINE.value:
                self.drawLine(obj)
            elif obj.twoDType.value == TwoDObjType.POLY.value:
                self.drawWireframe(obj)
            else:
                self.drawCurve(obj)
        self.drawSubCanvas()

    # desenha os eixos x e y; a porção que corresponte de [0, lenght] no eixo x é a reta de tom vermelho mais clara, e a
    # porção que representa [0, -lenght] é desenhada no tom vermelho escuro. a porção que corresponte de [0, height] no
    # eixo x é a reta de tom azul mais claro, e a porção que representa [0, -height] é desenhada no tom azul escuro.
    def drawExys(self):
        length, height = self.world.getWindow().getWindowDimensions()
        lines = list()
        # desenha linha de [0, lenght](direita) no eixo x - vermelho "claro"
        lines.append(Line('', [(0, 0), (length * 1000, 0)], color=(150, 0, 0)))
        # desenha linha de [0, -lenght](esquerda) no eixo x - vermelho "escuro"
        lines.append(Line('', [(0, 0), (-length * 1000, 0)], color=(51, 0, 0)))
        # desenha linha de [0, height](cima) no eixo y - azul "claro"
        lines.append(Line('', [(0, 0), (0, height * 1000)], color=(0, 0, 150)))
        # desenha linha de [0, -height](baixo) no eixo y - azul "escuro"
        lines.append(Line('', [(0, 0), (0, -height * 1000)], color=(0, 0, 51)))
        for line in lines:
            self.drawLine(line)

    # desenha um retangulo branco que corresponde à area da viewport
    def drawSubCanvas(self):
        p = QPainter()
        p.begin(self)
        p.setPen(QPen(Qt.black, 3, Qt.SolidLine, Qt.RoundCap, Qt.MiterJoin))
        p.drawLine(self.recuoViewport, self.recuoViewport, self.recuoViewport, self.viewportLenght - self.recuoViewport)
        p.drawLine(self.recuoViewport, self.viewportHeight - self.recuoViewport,
                   self.viewportLenght - self.recuoViewport, self.viewportHeight - self.recuoViewport)
        p.drawLine(self.viewportLenght - self.recuoViewport, self.viewportHeight - self.recuoViewport,
                   self.viewportLenght - self.recuoViewport, self.recuoViewport)
        p.drawLine(self.viewportLenght - self.recuoViewport, self.recuoViewport, self.recuoViewport, self.recuoViewport)
        p.end()

    # desenha um ponto
    def drawPoint(self, point: Point):
        # todo: clipar e normalizar antes de chamar a transformada
        p = QPainter()
        x, y = point.getX(), point.getY()
        x, y = self.world.getWindow().applySCN(x, y)
        # checa se o ponto é visivel na window; caso sim ele é desenhado
        if self.clippingAlg == 0 or (self.clippingAlg != 0 and (-1) < x < 1 and (-1) < y < 1):
            x, y = self.viewportTransform(x, y)
            p.begin(self)
            p.setPen(QPen(point.getColor(), 5, Qt.SolidLine, Qt.RoundCap, Qt.MiterJoin))
            p.drawPoint(x, y)
            p.end()

    # desenha uma linha
    def drawLine(self, line: Line):
        p = QPainter()
        x1, y1 = line.getX1_Y1()
        x2, y2 = line.getX2_Y2()
        # aplica o sistema de coordenadas normalizado para os pontos inicial e final da linha
        x1, y1 = self.world.getWindow().applySCN(x1, y1)
        x2, y2 = self.world.getWindow().applySCN(x2, y2)
        # realiza o cliping usando algum critério
        if self.clippingAlg == 1:
            line_coords = self.clippingCohenSutherland(x1, y1, x2, y2)
        elif self.clippingAlg == 2: # todo: alg cliping bryan
            line_coords = self.clippingLiangBarsky(x1, y1, x2, y2)
        else:
            line_coords = x1, y1, x2, y2
        # se as coordenadas forem todas 0, n deve desenhar a linha
        if line_coords == [0, 0, 0, 0]:
            return
        x1, y1, x2, y2 = line_coords
        # aplica a transformada de viewport para os pontos atualizados dessa linha
        x1, y1 = self.viewportTransform(x1, y1)
        x2, y2 = self.viewportTransform(x2, y2)
        p.begin(self)
        p.setPen(QPen(line.getColor(), 3, Qt.SolidLine, Qt.RoundCap, Qt.MiterJoin))
        p.drawLine(x1, y1, x2, y2)
        p.end()

    # desenha um poligono
    def drawWireframe(self, wireframe: Wireframe):
        p = QPainter()
        # p_ = QPainter()
        x1, y1 = wireframe.coords[0]
        x1, y1 = self.world.getWindow().applySCN(x1, y1)
        wire_coords = [(x1, y1)]
        for i in range(1, len(wireframe.coords)):
            x2, y2 = wireframe.coords[i]
            x2, y2 = self.world.getWindow().applySCN(x2, y2)
            wire_coords.append((x2, y2))

        # essa lista existe apenas para conter todos os poligonos que serão desenhados. Caso o clipping seja ligado
        # um poligono pode acabar virando multiplos sub poligonos.
        sub_polys = []
        if self.clippingAlg != 0:
            clipping_result = self.clippingWeilerAtherton(wire_coords=wire_coords)
            # caso em que o poly esta fora da viewport
            if clipping_result is None:
                return
            sub_polys.extend(clipping_result)
        else:
            sub_polys.append(wire_coords)
        # desenhas os poligonos na lista sub_polys
        p.begin(self)
        p.setPen(QPen(wireframe.getColor(), 3, Qt.SolidLine, Qt.RoundCap, Qt.MiterJoin))
        p.setBrush(QBrush(wireframe.getColor()))
        for sub_poly in sub_polys:
            x0, y0 = sub_poly[0]
            x0, y0 = self.viewportTransform(x0, y0)
            x1, y1 = x0, y0
            poly_points = [QPoint(x1, y1)]
            for i in range(1, len(sub_poly)):
                x2, y2 = sub_poly[i]
                x2, y2 = self.viewportTransform(x2, y2)
                poly_points.append(QPoint(x2, y2))
                p.drawLine(x1, y1, x2, y2)
                x1, y1 = x2, y2
            p.drawLine(x1, y1, x0, y0)
            p.drawPolygon(QPolygon(poly_points))
        p.end()

    def drawCurve(self, curve: BezierCurve):
        p = QPainter()
        x1, y1 = curve.coords[0]
        x1, y1 = self.world.getWindow().applySCN(x1, y1)
        curve_coords = [(x1, y1)]
        for i in range(1, len(curve.coords)):
            x2, y2 = curve.coords[i]
            x2, y2 = self.world.getWindow().applySCN(x2, y2)
            curve_coords.append((x2, y2))

        sub_curves = []

        if self.clippingAlg == 0:
            sub_curves.append(curve_coords)
        else:
            clippedCurve = self.clipCurve(curve_coords)
            # se a lista de linhas da curva clipada for nula, retorna
            if not clippedCurve:
                return
            sub_curves.extend(clippedCurve)
        p.begin(self)
        p.setPen(QPen(curve.getColor(), 3, Qt.SolidLine, Qt.RoundCap, Qt.MiterJoin))
        # desenha as linhas restantes do processo de clipping, se tiver ocorrido. ou a linha por completo
        for curve_lines in sub_curves:
            x1, y1 = curve_lines.pop(0)
            x1, y1 = self.viewportTransform(x1, y1)
            for x2, y2 in curve_lines:
                x2, y2 = self.viewportTransform(x2, y2)
                p.drawLine(x1, y1, x2, y2)
                x1, y1 = x2, y2
        p.end()

    def clipCurve(self, curve_coords: list):
        # lista com todas as sub curvas geradas pelo clipping
        sub_curves = []
        # lista com pontos q formam um sub curva da curva atual
        sub_curve = []
        x1, y1 = curve_coords.pop(0)
        # ainda n se sabe se a primeira linha esta dentro ou fora da window
        inside_window = False
        for p in curve_coords:
            x2, y2 = p
            # clipa a linha (x1, y1), (x2, y2)
            line_coords = self.clippingCohenSutherland(x1, y1, x2, y2)
            # se estiver dentro da window, adiciona a lista de pontos da sub curva atual
            if line_coords != (0, 0, 0, 0):
                x1, y1, x2, y2 = line_coords
                sub_curve.append((x1, y1))
                # o clipping retornou uma reta que tem as mesmas coordenadas de fim e inicio pq ela está na borda; nesse caso
                # salvar a sub curva atual e iniciar outra
                if (x1, y1) == (x2, y2):
                    sub_curves.append(sub_curve)
                    sub_curve = []
                    # restaura o valor do ponto (x2, y2) original para n ligar o fim dessa sub curva ao inicio da prox
                    x2, y2 = p
                    inside_window = False
                else:
                    inside_window = True
            # se n estiver, adiciona o ponto x1, y1 atual caso a sub curva atual tenha algum ponto, e logo apos a
            # adiciona s lista de sub curvas ja gerada; caso contrário n faz nada
            else:
                inside_window = False
                if sub_curve and -1 <= x1 <= 1 and -1 <= y1 <= 1:
                    sub_curve.append((x1, y1))
                    sub_curves.append(sub_curve)
                    sub_curve = []
            x1, y1 = x2, y2
        if inside_window:
            sub_curve.append((x1, y1))
            sub_curves.append(sub_curve)
            sub_curve = []
        return sub_curves



                # diminui a window
    def zoomIn(self):
        self.world.getWindow().zoomIn()
        self.update()

    # aumenta a window
    def zoomOut(self):
        self.world.getWindow().zoomOut()
        self.update()

    # move a window para cima
    def moveUp(self):
        self.world.getWindow().moveUp()
        self.update()

    # move a window para a direita
    def moveRight(self):
        self.world.getWindow().moveRight()
        self.update()

    # move a window para a esquerda
    def moveLeft(self):
        self.world.getWindow().moveLeft()
        self.update()

    # move a window para baixo
    def moveDown(self):
        self.world.getWindow().moveDown()
        self.update()

    # roda a window para a direita(sentido horario)
    def rotateRight(self):
        self.world.getWindow().rotateRight()
        self.update()

    # roda a window para a esquerda(sentido anti-horario)
    def rotateLeft(self):
        self.world.getWindow().rotateLeft()
        self.update()

    # adiciona um objento no mundo
    def addObj(self, obj: TwoDObj):
        self.world.objs.append(obj)
        self.update()

    # atualiza um objeto no mundo
    def updateObj(self, obj: TwoDObj):
        self.world.updateObj(obj)

    # deleta o objeto atualmente selecionado na interface
    def deleteObj(self, objName: str):
        try:
            self.world.deleteObj(self.world.getObj(objName))
            self.update()
        except:
            msg = QMessageBox()
            msg.setWindowTitle('Não há o que excluir')
            msg.setText(str('A liste de objetos ja está vazia.'))
            x = msg.exec_()

    # retorna o valor inteiro do RC usado no algoritmo de CohenSutherland
    def rcCodeToInt(self, code: list) -> int:
        value = 0
        for i in range(4):
            value = value + (2 ** code[i])
        return value

    # calcula o RC de um ponto qualquer, necessario no algoritmo de CohenSutherland
    # todo: checar qualquer algoritmo q tenha relação com esses valroes
    def calcRC(self, x: float, y: float,
               xwesq: float, ywtopo: float, xwdir: float, ywfundo: float) -> [int, int, int, int]:
        return [1 if y > ywtopo else 0,
                1 if y < ywfundo else 0,
                1 if x > xwdir else 0,
                1 if x < xwesq else 0]

    # Algoritmo Geral para Recorte de Linhas de Cohen-Sutherland. Retorna 0,0,0,0 caso a linha não seja visivel
    # considerando o tamanho atual da window; caso contrario retorna as coordenadas em uma lista, ajustadas na
    # considerando o tamanho atual da window; caso contrario retorna as coordenadas em uma lista, ajustadas na
    # ordem x1, y1, x2, y2.
    def clippingCohenSutherland(self, x1: float, y1: float, x2: float, y2: float) -> [float, float, float, float]:
        # xwesq, ywfundo, xwdir, ywtopo = self.world.getWindow().getCoords()
        xwesq, ywfundo = -1, -1
        xwdir, ywtopo = 1, 1
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

    def clippingLiangBarsky(self, x1: float, y1: float, x2: float, y2: float) -> [float, float, float, float]:
        xmin, ymin,= -1, -1
        xmax, ymax = 1, 1

        dx = x2 - x1
        dy = y2 - y1

        t0 = 0
        t1 = 1

        for edge in range(0, 4):
            if edge == 0:
                p = -dx
                q = -(xmin - x1)
            if edge == 1:
                p = dx
                q = (xmax - x1)
            if edge == 2:
                p = -dy
                q = -(ymin - y1)
            if edge == 3:
                p = dy
                q = (ymax - y1)

            r = q/p
            if p == 0 and q < 0:
                return 0, 0, 0, 0

            if p < 0:
                if r > t1:
                    return 0, 0, 0, 0
                elif r > t0:
                    t0 = r
            elif p > 0:
                if r < t0:
                    return 0, 0, 0, 0
                elif r < t1:
                    t1 = r
        x1 = x1 + t0 * dx
        y1 = y1 + t0 * dy

        x2 = x1 + t1 * dx
        y2 = y1 + t1 * dy

        return x1, y1, x2, y2
    
    # retorna o endereço que um ponto de intersecção deve ocupar na lista de coords do clippingPoly
    # retona dois valores, o primeiro é a lista na qual o ponto deve ser inserido, e o segundo o indice
    def serchPlaceInClippingPolyList(self, point, pontosTopo, pontosDireita, pontosFundo, pontosEsquerda) -> [int, int]:
        # checa se o ponto deve estar na lista do topo
        x, y = point
        x_1, y_1 = pontosTopo[0]
        x_2, _ = pontosTopo[len(pontosTopo) - 1]
        # esta no topo
        if y == y_1 and x_1 < x < x_2:
            for i in range(len(pontosTopo)):
                x_, _ = pontosTopo[i]
                if x < x_:
                    # elemento deve estar na lista de pontos do topo, na posicao i
                    return 1, i

        x_1, y_1 = pontosDireita[0]
        _, y_2 = pontosDireita[len(pontosDireita) - 1]
        # esta na direita
        if x == x_1 and y_1 > y > y_2:
            for i in range(len(pontosDireita)):
                _, y_ = pontosDireita[i]
                if y > y_:
                    # elemento deve estar na lista de pontos do topo, na posicao i
                    return 2, i

        x_1, y_1 = pontosFundo[0]
        x_2, _ = pontosFundo[len(pontosFundo) - 1]
        # esta no fundo
        if y == y_1 and x_1 > x > x_2:
            for i in range(len(pontosFundo)):
                x_, _ = pontosFundo[i]
                if x > x_:
                    # elemento deve estar na lista de pontos do topo, na posicao i
                    return 3, i

        x_1, y_1 = pontosEsquerda[0]
        _, y_2 = pontosEsquerda[len(pontosEsquerda) - 1]
        # esta na esquerda
        if x == x_1 and y_1 < y < y_2:
            for i in range(len(pontosEsquerda)):
                _, y_ = pontosEsquerda[i]
                if y < y_:
                    # elemento deve estar na lista de pontos da esquerda, na posicao i
                    return 4, i

        return -1, -1

    # Algoritmo de clipping de poligonos de Weiler Atherton. Retorna None caso nenhuma parte seja visivel; se houverem
    # partes visiveis elas sao retornadas em uma lista de subpoligonos.
    def clippingWeilerAtherton(self, wire_coords: list) -> list:
        # xvpesq, yvptopo, xvpdir, yvpfundo = self.getViewportCoords()
        xvpesq, yvpfundo = -1, -1
        yvptopo, xvpdir = 1, 1
        # dic com os RC codes de cada ponto do poligono
        RC = {point: self.calcRC(point[0], point[1], xvpesq, yvptopo, xvpdir, yvpfundo) for point in wire_coords}
        # lista de pontos da window, divididos em quatro listas: pontosEsquerda, pontosTopo, pontosDir e pontosFundo
        # essas listas serao usadas para compor a lista que contem os pontos da window e interseções geradas no proce
        # sso de clipping
        pontosTopo = [(xvpesq, yvptopo), (xvpdir, yvptopo)] # (-1,1) ~ (1,1)
        pontosDireita = [(xvpdir, yvptopo), (xvpdir, yvpfundo)] # (1,1) ~ (1,-1)
        pontosFundo = [(xvpdir, yvpfundo), (xvpesq, yvpfundo)] # (1,-1) ~ (-1,-1)
        pontosEsquerda = [(xvpesq, yvpfundo), (xvpesq, yvptopo)] # (-1,-1) ~ (-1,1)
        # dic de interseções de entrada na window
        in_intersec = []
        # dic de interseções de saida na window
        ou_intersec = []
        clipped_poly = []
        x1, y1 = wire_coords[0]
        clipped_poly.append((x1, y1))
        # x0, y0 = wire_coords[0]
        wire_coords.append((x1, y1))
        # Define os pontos de clipped_poly
        for i in range(1, len(wire_coords)):
            x2, y2 = wire_coords[i]
            # realiza o clipping de uma linha qualquer do poligono
            new_coords = self.clippingCohenSutherland(x1, y1, x2, y2)
            # se o retorno do alg de CohenSutherland for [0,0,0,0] significa q a linha esta fora da area da window, e
            # n gerou nenhum ponto de interseção
            if new_coords == (0, 0, 0, 0):
                clipped_poly.append((x2, y2))
                x1, y1 = x2, y2
                continue
            # a partir daqui o cenário é o seguinte: a linha está totalmente ou parcialmente dentro da window
            x1_, y1_, x2_, y2_ = new_coords
            new_x1y1 = False
            new_x2y2 = False
            # coord x1,y1 mudou
            if (x1, y1) != (x1_, y1_): # a iteracao anterior sempre introduz x1, y1
                # insere o ponto novo
                clipped_poly.append((x1_, y1_))
                # criou um ponto intermediario
                new_x1y1 = True

            # coord x2,y2 mudou, criou um ponto intermediario (x2_, y2_)
            if (x2, y2) != (x2_, y2_):
                # insere o ponto novo
                clipped_poly.append((x2_, y2_))
                # criou um ponto intermediario
                new_x2y2 = True

            # adiciona o ponto (x2, y2) a lista de pontos clipados;
            clipped_poly.append((x2, y2))

            # calcula rc do novo x1,y1, caso tenha sido criado
            RC_new_x1y1 = self.calcRC(x1_, y1_, xvpesq, yvptopo, xvpdir, yvpfundo) if new_x1y1 else None
            # calcula rc do novo x2,y2, caso tenha sido criado
            RC_new_x2y2 = self.calcRC(x2_, y2_, xvpesq, yvptopo, xvpdir, yvpfundo) if new_x2y2 else None

            # verifica se o novo x1,y1 é uma intersec de entrada ou saida, caso exista
            if new_x1y1:
                RC.update({(x1_, y1_): RC_new_x1y1})
                RC_x1 = RC[(x1, y1)]
                RC_x2 = RC_new_x2y2 if new_x2y2 else RC[(x2, y2)]
                # intersec entrando
                if RC_x1 != [0, 0, 0, 0] and RC_x2 == [0, 0, 0, 0]:
                    in_intersec.append((x1_, y1_))
                # intersec saindo
                else:
                    ou_intersec.append((x1_, y1_))
                # insere esse novo ponto em alguma das listas de coords da borda da window
                list_to_insert, index = self.serchPlaceInClippingPolyList((x1_, y1_), pontosTopo, pontosDireita,
                                                                          pontosFundo, pontosEsquerda)
                # insere na lista adequada, se o retorno for -1, -1 significa q o ponto é alguma das extremidades
                if list_to_insert == 1:
                    pontosTopo.insert(index, (x1_, y1_))
                elif list_to_insert == 2:
                    pontosDireita.insert(index, (x1_, y1_))
                elif list_to_insert == 3:
                    pontosFundo.insert(index, (x1_, y1_))
                elif list_to_insert == 4:
                    pontosEsquerda.insert(index, (x1_, y1_))
            # verifica se o novo x2,y2 é uma intersec de entrada ou saida, caso exista
            if new_x2y2:
                RC.update({(x2_, y2_): RC_new_x2y2})
                RC_x1 = RC[(x1_, y1_)] if new_x1y1 else RC[(x1, y1)]
                RC_x2 = RC[(x2, y2)]
                # intersec entrando
                if RC_x1 != [0, 0, 0, 0] and RC_x2 == [0, 0, 0, 0]:
                    in_intersec.append((x2_, y2_))
                # intersec saindo
                else:
                    ou_intersec.append((x2_, y2_))
                # insere esse novo ponto em alguma das listas de coords da borda da window
                list_to_insert, index = self.serchPlaceInClippingPolyList((x2_, y2_), pontosTopo,
                                                                          pontosDireita, pontosFundo, pontosEsquerda)
                # insere na lista adequada
                if list_to_insert == 1:
                    pontosTopo.insert(index, (x2_, y2_))
                elif list_to_insert == 2:
                    pontosDireita.insert(index, (x2_, y2_))
                elif list_to_insert == 3:
                    pontosFundo.insert(index, (x2_, y2_))
                elif list_to_insert == 4:
                    pontosEsquerda.insert(index, (x2_, y2_))
            x1, y1 = x2, y2

        # tirar ultimo elemento de clipped_poly, ele é repetido
        clipped_poly.pop()

        # define a lista de coords clipping_poly;
        clipping_poly = pontosTopo[:-1]
        clipping_poly.extend(pontosDireita[:-1])
        clipping_poly.extend(pontosFundo[:-1])
        clipping_poly.extend(pontosEsquerda[:-1])
        new_polys = []
        # se não tiver ponto de interseção de entrada ocorreram dois casos: o poligono está totalmente contido
        # dentro da window ou totalmente fora
        if not in_intersec:
            if all(RC[point] == [0, 0, 0, 0] for point in clipped_poly):
                return [clipped_poly]
            else:
                return None
        # copia da lista de pontos de entrada na window
        in_intersec_ = []
        in_intersec_.extend(in_intersec)
        visited = []
        # enquanto todos os pontos de entrada n tiverem sido visitados pelo menos uma vez
        while not len(visited) == len(in_intersec_):
            # pega o primeiro ponto de entrada na area da window e ja tira da lista de in_intersec
            p0 = in_intersec.pop(0)
            visited.append(p0)
            # lista de pontos do novo sub poly
            new_poly = [p0]
            # indice inicial
            index = (clipped_poly.index(p0) + 1) % len(clipped_poly)
            # andando pelas bordas do poly quando True; quando False, pelas bordas da window
            in_poly = True
            # percorre até achar o ponto de entrada p0
            while(1):
                if in_poly:
                    # adiciona o ponto a lista de pontos do novo sub poly
                    new_poly.append(clipped_poly[index])
                    # checa se o ponto adicionado é um ponto de saida da window
                    if clipped_poly[index] in ou_intersec:
                        # indice dentro da lista de pontos da borda da window
                        index = (clipping_poly.index(clipped_poly[index]) + 1) % len(clipping_poly)
                        # comeca a navegar pela lista de bordas da window
                        in_poly = False
                    else:
                        # atualiza o indice de maneira circular
                        index = (index + 1) % len(clipped_poly)
                else:
                    # se não for o ponto inicial, adiciona a lista de pontos do sub poly
                    if clipping_poly[index] != p0:
                        # atualiza o ponto a lista de pontos do novo sub poly
                        new_poly.append(clipping_poly[index])
                        # checa se o ponto adicionado é um ponto de entrada na window
                        if clipping_poly[index] in in_intersec_:
                            # adiciona o ponto de entrada a lista de visitados, caso ele ainda n tenha sido
                            if clipping_poly[index] not in visited:
                                visited.append(clipping_poly[index])
                            # indice dentro da lista de pontos do poly
                            index = (clipped_poly.index(clipping_poly[index]) + 1) % len(clipped_poly)
                            # comeca a navegar pela lista de pontos do poly
                            in_poly = True
                        else:
                            # atualiza o indice de maneira circular
                            index = (index + 1) % len(clipping_poly)
                    # fechou um poligono
                    else:
                        break
            # novo poly criado. adiciona a lista de polys a ser retornada
            new_polys.append(new_poly)
        return new_polys
