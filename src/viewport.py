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
        self.clippingAlg = 0

    # retorna os valores xy_vpmin e xy_pvmax
    def getViewportCoords(self) -> (float, float, float, float):
        # coords = self.visibleRegion().boundingRect().getCoords()
        xvpmin = self.recuoViewport - 1  # coordenadas da viewport começam em 0
        yvpmin = self.recuoViewport - 1  # coordenadas da viewport começam em 0
        xvpmax = self.viewportLenght - self.recuoViewport - 1  # coordenadas da viewport começam em 0
        yvpmax = self.viewportHeight - self.recuoViewport - 1  # coordenadas da viewport começam em 0
        return xvpmin, yvpmin, xvpmax, yvpmax

    # realiza a transformada de viewport para um ponto qualquer
    def viewportTransform(self, xw, yw) -> (float, float):
        # aplicar a matriz scn da window as coordenadas do mundo
        xw, yw = self.window_.applySCN(xw, yw)
        # realiza a transformada de viewport
        xwmin, ywmin, xwmax, ywmax = self.window_.getCoords()
        xwmin, ywmin = self.window_.applySCN(xwmin, ywmin)
        xwmax, ywmax = self.window_.applySCN(xwmax, ywmax)
        xvpmin, yvpmin, xvpmax, yvpmax = self.getViewportCoords()
        return ((xw - xwmin) / (xwmax - xwmin)) * (xvpmax - xvpmin),\
               (1 - ((yw - ywmin) / (ywmax - ywmin))) * (yvpmax - yvpmin)

    # método que é chamado toda vez que a viewport é atualizada via chamda de .update()
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

    # desenha os eixos x e y; a porção que corresponte de [0, lenght] no eixo x é a reta de tom vermelho mais clara, e a
    # porção que representa [0, -lenght] é desenhada no tom vermelho escuro. a porção que corresponte de [0, height] no
    # eixo x é a reta de tom azul mais claro, e a porção que representa [0, -height] é desenhada no tom azul escuro.
    def drawExys(self):
        p1 = QPainter()
        p2 = QPainter()
        p3 = QPainter()
        p4 = QPainter()
        length, height = self.window_.getWindowDimensions()
        length = length * self.viewportLenght
        height = height * self.viewportHeight
        x1, y1 = self.viewportTransform(0, 0)
        # desenha linha de [0, lenght](direita) no eixo x - vermelho "claro"
        x2, y2 = self.viewportTransform(length, 0)
        if self.clippingAlg == 1:
            line_coords = self.clippingCohenSutherland(x1, y1, x2, y2)
        elif self.clippingAlg == 2: # todo: outro alg clipping
            line_coords = self.clippingCohenSutherland(x1, y1, x2, y2)
        else:
            line_coords = [x1, y1, x2, y2]
        if line_coords != [0, 0, 0, 0]:
            x1, y1, x2, y2 = line_coords
            p1.begin(self)
            p1.setPen(QPen(QColor(150, 0, 0, 255), 4))
            p1.drawLine(x1, y1, x2, y2)
            p1.end()
        # desenha linha de [0, -lenght](esquerda) no eixo x - vermelho "escuro"
        x2, y2 = self.viewportTransform(-length, 0)
        if self.clippingAlg == 1:
            line_coords = self.clippingCohenSutherland(x1, y1, x2, y2)
        elif self.clippingAlg == 2: # todo: outro alg clipping
            line_coords = self.clippingCohenSutherland(x1, y1, x2, y2)
        else:
            line_coords = [x1, y1, x2, y2]
        if line_coords != [0, 0, 0, 0]:
            x1, y1, x2, y2 = line_coords
            p2.begin(self)
            p2.setPen(QPen(QColor(51, 0, 0, 255), 3))
            p2.drawLine(x1, y1, x2, y2)
            p2.end()
        # desenha linha de [0, height](cima) no eixo y - azul "claro"
        x2, y2 = self.viewportTransform(0, height)
        if self.clippingAlg == 1:
            line_coords = self.clippingCohenSutherland(x1, y1, x2, y2)
        elif self.clippingAlg == 2: # todo: outro alg clipping
            line_coords = self.clippingCohenSutherland(x1, y1, x2, y2)
        else:
            line_coords = [x1, y1, x2, y2]
        if line_coords != [0, 0, 0, 0]:
            x1, y1, x2, y2 = line_coords
            p3.begin(self)
            p3.setPen(QPen(QColor(0, 0, 150, 255), 4))
            p3.drawLine(x1, y1, x2, y2)
            p3.end()
        # desenha linha de [0, -height](baixo) no eixo y - azul "escuro"
        x2, y2 = self.viewportTransform(0, -height)
        if self.clippingAlg == 1:
            line_coords = self.clippingCohenSutherland(x1, y1, x2, y2)
        elif self.clippingAlg == 2: # todo: outro alg clipping
            line_coords = self.clippingCohenSutherland(x1, y1, x2, y2)
        else:
            line_coords = [x1, y1, x2, y2]
        if line_coords != [0, 0, 0, 0]:
            x1, y1, x2, y2 = line_coords
            p4.begin(self)
            p4.setPen(QPen(QColor(0, 0, 51, 255), 3))
            p4.drawLine(x1, y1, x2, y2)
            p4.end()

    # desenha um retangulo branco que corresponde à area da viewport
    def drawSubCanvas(self):
        p = QPainter()
        p.begin(self)
        p.setPen(QPen(Qt.white, 3, Qt.SolidLine, Qt.RoundCap, Qt.MiterJoin))
        p.drawLine(self.recuoViewport, self.recuoViewport, self.recuoViewport, self.viewportLenght - self.recuoViewport)
        p.drawLine(self.recuoViewport, self.viewportHeight - self.recuoViewport,
                   self.viewportLenght - self.recuoViewport, self.viewportHeight - self.recuoViewport)
        p.drawLine(self.viewportLenght - self.recuoViewport, self.viewportHeight - self.recuoViewport,
                   self.viewportLenght - self.recuoViewport, self.recuoViewport)
        p.drawLine(self.viewportLenght - self.recuoViewport, self.recuoViewport, self.recuoViewport, self.recuoViewport)
        p.end()

    # desenha um ponto
    def drawPoint(self, point: Point):
        p = QPainter()
        x, y = self.viewportTransform(point.getX(), point.getY())
        xesq, ytopo, xdir, yfundo = self.getViewportCoords()
        # checa se o ponto é visivel na window; caso sim ele é desenhado
        if xesq < x < xdir and yfundo > y > ytopo:
            p.begin(self)
            p.setPen(QPen(point.getColor(), 5, Qt.SolidLine, Qt.RoundCap, Qt.MiterJoin))
            p.drawPoint(x, y)
            p.end()

    # desenha uma linha
    def drawLine(self, line: Line):
        p = QPainter()
        x1, y1 = line.getX1_Y1()
        x1, y1 = self.viewportTransform(x1, y1)
        x2, y2 = line.getX2_Y2()
        x2, y2 = self.viewportTransform(x2, y2)
        # realiza o clipping usando algum critério
        if self.clippingAlg == 1:
            line_coords = self.clippingCohenSutherland(x1, y1, x2, y2)
        elif self.clippingAlg == 2: # todo: outro alg clipping
            line_coords = self.clippingCohenSutherland(x1, y1, x2, y2)
        else:
            line_coords = x1, y1, x2, y2
        # se as coordenadas forem todas 0, n deve desenhar a linha
        if line_coords == [0, 0, 0, 0]:
            return
        x1, y1, x2, y2 = line_coords
        p.begin(self)
        p.setPen(QPen(line.getColor(), 3, Qt.SolidLine, Qt.RoundCap, Qt.MiterJoin))
        p.drawLine(x1, y1, x2, y2)
        p.end()

    # desenha um poligono
    def drawWireframe(self, wireframe: Wireframe):
        p = QPainter()
        # p_ = QPainter()
        x1, y1 = wireframe.coords[0]
        x1, y1 = self.viewportTransform(x1, y1)
        wire_coords = [(x1, y1)]
        # poly_points = [QPoint(x1, y1)]
        for i in range(1, len(wireframe.coords)):
            x2, y2 = wireframe.coords[i]
            x2, y2 = self.viewportTransform(x2, y2)
            wire_coords.append((x2, y2))
            # poly_points.append(QPoint(x2, y2))
        sub_polys = self.clippingWeilerAtherton(wire_coords=wire_coords)
        # caso em que o poly esta fora da viewport
        if sub_polys is None:
            return
        # desenhas os sub-poligonos gerados
        p.begin(self)
        p.setPen(QPen(wireframe.getColor(), 3, Qt.SolidLine, Qt.RoundCap, Qt.MiterJoin))
        p.setBrush(QBrush(wireframe.getColor()))
        for sub_poly in sub_polys:
            x0, y0 = sub_poly[0]
            x1, y1 = x0, y0
            poly_points = [QPoint(x1, y1)]
            for i in range(1, len(sub_poly)):
                x2, y2 = sub_poly[i]
                poly_points.append(QPoint(x2, y2))
                p.drawLine(x1, y1, x2, y2)
                x1, y1 = x2, y2
            poly_points.append(QPoint(x0, y0))
            p.drawLine(x1, y1, x0, y0)
            p.drawPolygon(QPolygon(poly_points))
        p.end()
        # preenche o poligono. Talvez tenha q mudar se não der para fazer isso.
        # p_.begin(self)
        # p_.setBrush(QBrush(wireframe.getColor()))
        # p_.drawPolygon(QPolygon(poly_points))
        # p_.end()

    # diminui a window
    def zoomIn(self):
        self.window_.zoomIn()
        self.update()

    # aumenta a window
    def zoomOut(self):
        self.window_.zoomOut()
        self.update()

    # move a window para cima
    def moveUp(self):
        self.window_.moveUp()
        self.update()

    # move a window para a direita
    def moveRight(self):
        self.window_.moveRight()
        self.update()

    # move a window para a esquerda
    def moveLeft(self):
        self.window_.moveLeft()
        self.update()

    # move a window para baixo
    def moveDown(self):
        self.window_.moveDown()
        self.update()

    # roda a window para a direita(sentido horario)
    def rotateRight(self):
        self.window_.rotateRight()
        self.update()

    # roda a window para a esquerda(sentido anti-horario)
    def rotateLeft(self):
        self.window_.rotateLeft()
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
    def calcRC(self, x: float, y: float,
               xwesq: float, ywtopo: float, xwdir: float, ywfundo: float) -> [int, int, int, int]:
        return [1 if y < ywtopo else 0, # viewport tem eixo y invertido
                1 if y > ywfundo else 0, # viewport tem eixo y invertido
                1 if x > xwdir else 0,
                1 if x < xwesq else 0]

    # Algoritmo Geral para Recorte de Linhas de Cohen-Sutherland. Retorna 0,0,0,0 caso a linha não seja visivel
    # considerando o tamanho atual da viewport; caso contrario retorna as coordenadas em uma lista, ajustadas na
    # ordem x1, y1, x2, y2.
    def clippingCohenSutherland(self, x1: float, y1: float, x2: float, y2: float) -> [float, float, float, float]:
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
        if x == x_1 and y_1 < y < y_2:  # eixo y invertido na viewport
            for i in range(len(pontosDireita)):
                _, y_ = pontosDireita[i]
                if y < y_:
                    # elemento deve estar na lista de pontos do topo, na posicao i
                    return 2, i

        x_1, y_1 = pontosFundo[0]
        x_2, _ = pontosFundo[len(pontosFundo) - 1]
        # esta no fundo
        if y == y_1 and x_1 < x < x_2:
            for i in range(len(pontosFundo)):
                x_, _ = pontosFundo[i]
                if x > x_:
                    # elemento deve estar na lista de pontos do topo, na posicao i
                    return 3, i

        # esta na esquerda
        for i in range(len(pontosEsquerda)):
            _, y_ = pontosEsquerda[i]
            if y > y_:
                # elemento deve estar na lista de pontos da esquerda, na posicao i
                return 4, i

    # Algoritmo de clipping de poligonos de Weiler Atherton. Retorna None caso nenhuma parte seja visivel; se houverem
    # partes visiveis elas sao retornadas em uma lista de subpoligonos.
    def clippingWeilerAtherton(self, wire_coords: list) -> list:
        xvpesq, yvptopo, xvpdir, yvpfundo = self.getViewportCoords()
        # dic com os RC codes de cada ponto do poligono
        RC = {point: self.calcRC(point[0], point[1], xvpesq, yvptopo, xvpdir, yvpfundo) for point in wire_coords}
        # lista de pontos da viewport, divididos em quatro listas: pontosEsquerda, pontosTopo, pontosDir e pontosFundo
        # essas listas serao usadas para compor a lista que contem os pontos da viewport e interseções geradas no proce
        # sso de clipping
        pontosTopo = [(xvpesq, yvptopo), (xvpdir, yvptopo)]
        pontosDireita = [(xvpdir, yvptopo), (xvpdir, yvpfundo)]
        pontosFundo = [(xvpdir, yvpfundo), (xvpesq, yvpfundo)]
        pontosEsquerda = [(xvpesq, yvpfundo), (xvpesq, yvptopo)]
        # dic de interseções de entrada na viewport
        in_intersec = []
        # dic de interseções de saida na viewport
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
            # se o retorno do alg de CohenSutherland for [0,0,0,0] significa q a linha esta fora da area da viewport, e
            # n gerou nenhum ponto de interseção
            if new_coords == (0, 0, 0, 0):
                clipped_poly.append((x2, y2))
                x1, y1 = x2, y2
                continue
            # a partir daqui o cenário é o seguinte: a linha está totalmente ou parcialmente fora da viewport
            x1_, y1_, x2_, y2_ = new_coords
            new_x1y1 = False
            new_x2y2 = False
            # coord x1,y1 mudou
            if (x1, y1) != (x1_, y1_): # a iteracao anterior sempre introduz x1, y1, caso n tenha mudado
                # criou um ponto intermediario
                new_x1y1 = True
                # insere o ponto novo
                clipped_poly.append((x1_, y1_))

            # coord x2,y2 n mudou
            if (x2, y2) == (x2_, y2_):
                clipped_poly.append((x2, y2))
            # coord x2,y2 mudou
            else:
                new_x2y2 = True
                # insere o ponto novo
                clipped_poly.append((x2_, y2_))
                # criou um ponto intermediario
                clipped_poly.append((x2, y2))

            # calcula rc do novo x1,y1, caso tenha sido criado
            RC_new_x1y1 = self.calcRC(x1_, y1_, xvpesq, yvptopo, xvpdir, yvpfundo) if new_x1y1 else None
            # calcula rc do novo x2,y2, caso tenha sido criado
            RC_new_x2y2 = self.calcRC(x2_, y2_, xvpesq, yvptopo, xvpdir, yvpfundo) if new_x2y2 else None

            # verifica se o novo x1,y1 é uma intersec de entrada ou saida, caso exista
            if new_x1y1:
                RC_x1 = RC[(x1, y1)]
                RC_x2 = RC_new_x2y2 if new_x2y2 else RC[(x2, y2)]
                # intersec entrando
                if RC_x1 != [0, 0, 0, 0] and RC_x2 == [0, 0, 0, 0]:
                    in_intersec.append((x1_, y1_))
                # intersec saindo
                else:
                    ou_intersec.append((x1_, y1_))
                # insere esse novo ponto em alguma das listas de coords da borda da viewport
                list_to_insert, index = self.serchPlaceInClippingPolyList((x1_, y1_), pontosTopo, pontosDireita,
                                                                          pontosFundo, pontosEsquerda)
                # insere na lista adequada
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
                RC_x1 = RC_new_x1y1 if new_x1y1 else RC[(x1, y1)]
                RC_x2 = RC[(x2, y2)]
                # intersec entrando
                if RC_x1 != [0, 0, 0, 0] and RC_x2 == [0, 0, 0, 0]:
                    in_intersec.append((x2_, y2_))
                # intersec saindo
                else:
                    ou_intersec.append((x2_, y2_))
                # insere esse novo ponto em alguma das listas de coords da borda da viewport
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
        # dentro da viewport ou totalmente fora
        if not in_intersec:
            if all(RC[point] == [0, 0, 0, 0] for point in clipped_poly):
                return [clipped_poly]
            else:
                return None
        # copia da lista de pontos de entrada na viewport
        in_intersec_ = []
        in_intersec_.extend(in_intersec)
        visited = []
        # enquanto todos os pontos de entrada n tiverem sido visitados pelo menos uma vez
        while not len(visited) == len(in_intersec_):
            # pega o primeiro ponto de entrada na area da viewport e ja tira da lista de in_intersec
            p0 = in_intersec.pop(0)
            visited.append(p0)
            # lista de pontos do novo sub poly
            new_poly = [p0]
            # indice inicial
            index = (clipped_poly.index(p0) + 1) % len(clipped_poly)
            # andando pelas bordas do poly quando True; quando False, pelas bordas da viewport
            in_poly = True
            # percorre até achar o ponto de entrada p0
            while(1):
                if in_poly:
                    # adiciona o ponto a lista de pontos do novo sub poly
                    new_poly.append(clipped_poly[index])
                    # checa se o ponto adicionado é um ponto de saida da viewport
                    if clipped_poly[index] in ou_intersec:
                        # indice dentro da lista de pontos da borda da viewport
                        index = (clipping_poly.index(clipped_poly[index]) + 1) % len(clipping_poly)
                        # comeca a navegar pela lista de bordas da viewport
                        in_poly = False
                        continue
                    # atualiza o indice de maneira circular
                    index = (index + 1) % len(clipped_poly)
                else:
                    # se não for o ponto inicial, adiciona a lista de pontos do sub poly
                    if clipping_poly[index] != p0:
                        # atualiza o ponto a lista de pontos do novo sub poly
                        new_poly.append(clipping_poly[index])
                        # checa se o ponto adicionado é um ponto de entrada na viewport
                        if clipping_poly[index] in in_intersec_:
                            # adiciona o ponto de entrada a lista de visitados, caso ele ainda n tenha sido
                            if clipping_poly[index] not in visited:
                                visited.append(clipping_poly[index])
                            # indice dentro da lista de pontos do poly
                            index = (clipped_poly.index(clipping_poly[index]) + 1) % len(clipped_poly)
                            # comeca a navegar pela lista de pontos do poly
                            in_poly = True
                            continue
                        # atualiza o indice de maneira circular
                        index = (index + 1) % len(clipping_poly)
                    # fechou um poligono
                    else:
                        break
            # novo poly criado. adiciona a lista de polys a ser retornada
            new_polys.append(new_poly)
        return new_polys
