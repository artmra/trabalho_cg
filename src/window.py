import numpy

from objs import Line


class Window:
    # construtor
    def __init__(self, world, xyw_min=None, xyw_max=None):
        self.world = world
        # caso em q é None
        if xyw_min is None or xyw_max is None:
            self.xyw_min = (-100, -100)
            self.xyw_max = (100, 100)
        # caso em q n é None
        else:
            if not isinstance(xyw_min, tuple) or len(xyw_min) != 2:
                raise Exception('O param xyw_min deve ser uma tupla de 2 valores.')
            try:
                self.xyw_min = (float(xyw_min[0]), float(xyw_min[1]))
            except Exception:
                raise Exception('As coordenadas xyw_min devem ser pares de números.')

            if not isinstance(xyw_max, tuple) or len(xyw_max) != 2:
                raise Exception('O param xyw_max deve ser uma tupla de 2 valores.')
            try:
                self.xyw_max = (float(xyw_max[0]), float(xyw_max[1]))
            except Exception:
                raise Exception('As coordenadas xyw_max devem ser pares de números.')
        self.xyw_1 = self.xyw_min
        self.xyw_2 = (self.xyw_max[0], self.xyw_min[1])
        self.xyw_3 = (self.xyw_min[0], self.xyw_max[1])
        self.xyw_4 = self.xyw_max
        # define o centro original da window(attr q pode ser usado para trazer a view de volta ao seu centro original)
        self.center = self.calcCenter()
        # define o novo centro(var que pode ser utilizada em futuros calculos envolvendo o centro da window)
        self.newCenter = self.center
        self.fatorMovimento = 10
        self.window_scn = numpy.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        # inicializa scn da window
        self.degrees = 0
        self.scn()

    # retorna as coordenadas (x,y) do centro da window
    def calcCenter(self) -> (float, float):
        return (self.xyw_min[0] + self.xyw_max[0]) / 2, (self.xyw_min[1] + self.xyw_max[1]) / 2

    # retorna as coordenadas do canto inferior esquerdo e canto superior direito da window
    def getCoords(self) -> (float, float, float, float):
        return self.xyw_min[0], self.xyw_min[1], self.xyw_max[0], self.xyw_max[1]

    # retorna a largura e profundidade da window
    def getWindowDimensions(self) -> (float, float):
        xyw1 = numpy.array([self.xyw_1[0], self.xyw_1[1]])
        xyw2 = numpy.array([self.xyw_2[0], self.xyw_2[1]])
        xyw3 = numpy.array([self.xyw_3[0], self.xyw_3[1]])
        return numpy.linalg.norm(xyw2 - xyw1), numpy.linalg.norm(xyw3 - xyw1)

    # translada a window para cima, do ponto de vista do usuario
    def moveUp(self):
        # se grau de inclinação da window for maior que 180, inverter sinal do param
        invert = -1 if self.degrees > 180 else 1
        # se grau estiver na faixa [60, 120] ou [210, 330] o eixo movimentado deve ser trocado
        if (60 < self.degrees < 180) or (210 < self.degrees < 330):
            self._translate(dx=invert * self.fatorMovimento)
        else:
            self._translate(dy=invert * self.fatorMovimento)

    # translada a window para baixo, do ponto de vista do usuario
    def moveDown(self):
        # se grau de inclinação da window for maior que 180, inverter sinal do param
        invert = -1 if self.degrees > 180 else 1
        # se grau estiver na faixa [60, 120] ou [210, 330] o eixo movimentado deve ser trocado
        if (60 < self.degrees < 180) or (210 < self.degrees < 330):
            self._translate(dx=invert * (-1) * self.fatorMovimento)
        else:
            self._translate(dy=invert * (-1) * self.fatorMovimento)

    # translada a window para direita, do ponto de vista do usuario
    def moveRight(self):
        # se grau de inclinação da window for maior que 180, inverter sinal do param
        invert = -1 if self.degrees > 180 else 1
        # se grau estiver na faixa [60, 120] ou [210, 330] o eixo movimentado deve ser trocado
        if (60 < self.degrees < 180) or (210 < self.degrees < 330):
            self._translate(dy=invert * self.fatorMovimento)
        else:
            self._translate(dx=invert * self.fatorMovimento)

    # translada a window para esquerda, do ponto de vista do usuario
    def moveLeft(self):
        # se grau de inclinação da window for maior que 180, inverter sinal do param
        invert = -1 if self.degrees > 180 else 1
        # se grau estiver na faixa [60, 120] ou [210, 330] o eixo movimentado deve ser trocado
        if (60 < self.degrees < 180) or (210 < self.degrees < 330):
            self._translate(dy=invert * (-1) * self.fatorMovimento)
        else:
            self._translate(dx=invert * (-1) * self.fatorMovimento)

    # realiza a translaçao da window
    def _translate(self, dx=0, dy=0):
        # cria a matriz de translacao do obj para um dx e dy qualquer
        window_coords = numpy.array([[self.xyw_1[0], self.xyw_1[1], 1],
                                     [self.xyw_2[0], self.xyw_2[1], 1],
                                     [self.xyw_3[0], self.xyw_3[1], 1],
                                     [self.xyw_4[0], self.xyw_4[1], 1]])
        # realiza a translacao
        translate_matrix = numpy.array([[1, 0, 0], [0, 1, 0], [dx, dy, 1]])
        # atualiza a window
        xyw_1, xyw_2, xyw_3, xyw_4 = numpy.matmul(window_coords, translate_matrix)
        self.xyw_1 = (xyw_1[0], xyw_1[1])
        self.xyw_2 = (xyw_2[0], xyw_2[1])
        self.xyw_3 = (xyw_3[0], xyw_3[1])
        self.xyw_4 = (xyw_4[0], xyw_4[1])
        self.xyw_min = self.xyw_1
        self.xyw_max = self.xyw_4
        # atualiza o centro
        self.newCenter = self.calcCenter()
        # atualiza scn
        self.scn()

    # Encolhe a window
    def zoomIn(self):
        self._scale(scale=0.9)
        self.fatorMovimento = self.fatorMovimento * 0.9

    # Aumenta a window
    def zoomOut(self):
        self._scale(scale=1.1)
        self.fatorMovimento = self.fatorMovimento * 1.1

    # Escalona a window
    def _scale(self, scale=1):
        # centro do obj
        cx, cy = self.newCenter
        # coords do mundo
        window_coords = numpy.array([[self.xyw_1[0], self.xyw_1[1], 1],
                                     [self.xyw_2[0], self.xyw_2[1], 1],
                                     [self.xyw_3[0], self.xyw_3[1], 1],
                                     [self.xyw_4[0], self.xyw_4[1], 1]])
        # ajusta o centro do mundo com o obj
        translate_matrix_1 = numpy.array([[1, 0, 0], [0, 1, 0], [(-1) * cx, (-1) * cy, 1]])
        # realiza o escalonamento(num sei se esse e o termo correto)
        scale_matrix = numpy.array([[scale, 0, 0], [0, scale, 0], [0, 0, 1]])
        # reverte o ajuste do centro do mundo com o obj
        translate_matrix_2 = numpy.array([[1, 0, 0], [0, 1, 0], [cx, cy, 1]])
        # monta uma matriz que aplica todas as transformacoes
        transformations = numpy.matmul(translate_matrix_1, scale_matrix)
        transformations = numpy.matmul(transformations, translate_matrix_2)
        # aplica as transformacoes
        xyw_1, xyw_2, xyw_3, xyw_4 = numpy.matmul(window_coords, transformations)
        # atualiza xyw_min/max
        self.xyw_1 = (xyw_1[0], xyw_1[1])
        self.xyw_2 = (xyw_2[0], xyw_2[1])
        self.xyw_3 = (xyw_3[0], xyw_3[1])
        self.xyw_4 = (xyw_4[0], xyw_4[1])
        self.xyw_min = self.xyw_1
        self.xyw_max = self.xyw_4
        # atualiza o centro
        self.newCenter = self.calcCenter()
        # atualiza scn
        self.scn()

    # Rotaciona a window no sentido horario
    def rotateRight(self):
        # 360 - 10 = 350
        self._rotate(350)

    # Rotaciona a window no sentido anti-horario
    def rotateLeft(self):
        self._rotate(10)

    # Rotaciona a window em relaçao ao seu proprio centro
    def _rotate(self, angle=0):
        self.degrees = (self.degrees + angle) % 360
        # centro do obj
        cx, cy = self.newCenter
        # coords do mundo
        window_coords = numpy.array([[self.xyw_1[0], self.xyw_1[1], 1],
                                     [self.xyw_2[0], self.xyw_2[1], 1],
                                     [self.xyw_3[0], self.xyw_3[1], 1],
                                     [self.xyw_4[0], self.xyw_4[1], 1]])
        # ajusta o centro do mundo com o obj
        translate_matrix_1 = numpy.array([[1, 0, 0], [0, 1, 0], [(-1) * cx, (-1) * cy, 1]])
        # realiza a rotacao
        radians = numpy.radians(angle)
        sin = numpy.sin(radians)
        cos = numpy.cos(radians)
        rotate_matrix = numpy.array([[cos, -sin, 0], [sin, cos, 0], [0, 0, 1]])
        # reverte a transformacao feita
        translate_matrix_2 = numpy.array([[1, 0, 0], [0, 1, 0], [cx, cy, 1]])
        # gera a matriz de transformacao de rotacao
        transformations = numpy.matmul(translate_matrix_1, rotate_matrix)
        transformations = numpy.matmul(transformations, translate_matrix_2)
        # aplica as transformacoes
        xyw_1, xyw_2, xyw_3, xyw_4 = numpy.matmul(window_coords, transformations)
        # atualiza xyw_min/max
        self.xyw_1 = (xyw_1[0], xyw_1[1])
        self.xyw_2 = (xyw_2[0], xyw_2[1])
        self.xyw_3 = (xyw_3[0], xyw_3[1])
        self.xyw_4 = (xyw_4[0], xyw_4[1])
        self.xyw_min = self.xyw_1
        self.xyw_max = self.xyw_4
        # atualiza o centro
        self.newCenter = self.calcCenter()
        # atualiza scn
        self.scn()

    # Calcula a matriz de transformaçao de sistemas de coordenadas da window
    def scn(self):
        # centro do obj
        cx, cy = self.newCenter
        # ajusta o centro do mundo com o obj
        translate_matrix_1 = numpy.array([[1, 0, 0], [0, 1, 0], [(-1) * cx, (-1) * cy, 1]])
        # pega ao INVERSO da rotacao atual da window
        radians = numpy.radians((-1) * self.degrees)
        sin = numpy.sin(radians)
        cos = numpy.cos(radians)
        # rotaciona
        rotate_matrix = numpy.array([[cos, -sin, 0], [sin, cos, 0], [0, 0, 1]])
        length, height = self.getWindowDimensions()
        sx = 1 / (length / 2)
        sy = 1 / (height / 2)
        # realiza o escalonamento(num sei se esse e o termo correto)
        scale_matrix = numpy.array([[sx, 0, 0], [0, sy, 0], [0, 0, 1]])
        # gera a matriz de conversao para scn da window
        scn = numpy.matmul(translate_matrix_1, rotate_matrix)
        self.window_scn = numpy.matmul(scn, scale_matrix)

    # Aplica a matriz de transformaçao de sistema de coordenadas da window a um ponto qualquer
    def applySCN(self, x, y):
        point_coords = numpy.array([x, y, 1])
        final_coords = numpy.matmul(point_coords, self.window_scn)
        return final_coords[0], final_coords[1]
