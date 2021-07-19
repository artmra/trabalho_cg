import numpy

from src.objs import TwoDObj


class Window:
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
        # # todo: inicializa scn
        self.scn()

    def calcCenter(self) -> tuple:
        # todo: mudar para uma implementacao mais "correta"
        return ((self.xyw_min[0] + self.xyw_max[0]) / 2, (self.xyw_min[1] + self.xyw_max[1]) / 2)

    def getCoords(self) -> tuple:
        return self.xyw_min[0], self.xyw_min[1], self.xyw_max[0], self.xyw_max[1]

    def getWindowDimensions(self):
        xyw1 = numpy.array([self.xyw_1[0], self.xyw_1[1]])
        xyw2 = numpy.array([self.xyw_2[0], self.xyw_2[1]])
        xyw3 = numpy.array([self.xyw_3[0], self.xyw_3[1]])
        return numpy.linalg.norm(xyw2 - xyw1), numpy.linalg.norm(xyw3 - xyw1)

    def moveUp(self):
        self._translate(dy=self.fatorMovimento)

    def moveDown(self):
        self._translate(dy=(-1)*self.fatorMovimento)

    def moveRight(self):
        self._translate(dx=self.fatorMovimento)

    def moveLeft(self):
        self._translate(dx=(-1)*self.fatorMovimento)

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
        # atualiza scn
        self.scn()
        # atualiza o centro
        self.newCenter = self.calcCenter()

    def zoomIn(self):
        self._scale(scale=0.9)
        self.fatorMovimento = self.fatorMovimento * 0.9

    def zoomOut(self):
        self._scale(scale=1.1)
        self.fatorMovimento = self.fatorMovimento * 1.1

    # escala um obj
    def _scale(self, scale=1):
        # centro do obj
        cx, cy = self.newCenter
        # coords do mundo
        window_coords = numpy.array([[self.xyw_1[0], self.xyw_1[1], 1],
                                     [self.xyw_2[0], self.xyw_2[1], 1],
                                     [self.xyw_3[0], self.xyw_3[1], 1],
                                     [self.xyw_4[0], self.xyw_4[1], 1]])
        # ajusta o centro do mundo com o obj
        translate_matrix_1 = numpy.array([[1, 0, 0], [0, 1, 0], [(-1)*cx, (-1)*cy, 1]])
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
        # atualiza scn
        self.scn()
        # atualiza o centro
        self.newCenter = self.calcCenter()

    # rotacionar no sentido horario
    def rotateRight(self):
        self._rotate(-10)

    # rotacionar no sentido anti-horario
    def rotateLeft(self):
        self._rotate(10)

    # rotaciona o obj em relacao a algum referencial
    def _rotate(self, angle=0):
        # centro do obj
        cx, cy = self.newCenter
        # coords do mundo
        window_coords = numpy.array([[self.xyw_1[0], self.xyw_1[1], 1],
                                     [self.xyw_2[0], self.xyw_2[1], 1],
                                     [self.xyw_3[0], self.xyw_3[1], 1],
                                     [self.xyw_4[0], self.xyw_4[1], 1]])
        # ajusta o centro do mundo com o obj
        translate_matrix_1 = numpy.array([[1, 0, 0], [0, 1, 0], [(-1)*cx, (-1)*cy, 1]])
        # realiza a rotacao
        sin = numpy.sin(angle * numpy.pi / 180)
        cos = numpy.cos(angle * numpy.pi / 180)
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
        # atualiza scn
        self.scn()
        # atualiza o centro
        self.newCenter = self.calcCenter()

    def scn(self):
        # centro do obj
        cx, cy = self.newCenter
        xyw1 = numpy.array([self.xyw_1[0], self.xyw_1[1]])
        xyw2 = numpy.array([self.xyw_2[0], self.xyw_2[1]])
        xyw3 = numpy.array([self.xyw_3[0], self.xyw_3[1]])
        xyw4 = numpy.array([self.xyw_4[0], self.xyw_4[1]])
        # coords do ponto medio superior da window, q sera usado pra definir o vup okay
        aux = numpy.array([[(xyw3[0] + xyw4[0])/2, (xyw3[1] + xyw4[1])/2, 1]])
        # ajusta o centro do mundo com o obj
        translate_matrix_1 = numpy.array([[1, 0, 0], [0, 1, 0], [(-1) * cx, (-1) * cy, 1]])
        # realiza a rotacao para alinhar o vup com o eixo y
        aux = numpy.matmul(aux, translate_matrix_1)
        vup = numpy.array([aux[0][0], aux[0][1]])
        # normaliza vup
        vup = vup / numpy.linalg.norm(vup)
        y = numpy.array([0, 1])
        # calcula o angulo
        cos_angle = numpy.inner(y, vup)/(numpy.linalg.norm(vup)*numpy.linalg.norm(y))
        angle = numpy.arccos(cos_angle)
        sin = numpy.sin(angle * numpy.pi / 180)
        cos = numpy.cos(angle * numpy.pi / 180)
        rotate_matrix = numpy.array([[cos, -sin, 0], [sin, cos, 0], [0, 0, 1]])
        # https://stackoverflow.com/questions/1401712/how-can-the-euclidean-distance-be-calculated-with-numpy
        length, height = self.getWindowDimensions()
        sx = 1 / (length / 2)
        sy = 1 / (height / 2)
        # realiza o escalonamento(num sei se esse e o termo correto)
        scale_matrix = numpy.array([[sx, 0, 0], [0, sy, 0], [0, 0, 1]])
        # gera a matriz de transformacao de rotacao
        self.window_scn = numpy.matmul(translate_matrix_1, rotate_matrix)
        self.window_scn = numpy.matmul(self.window_scn, scale_matrix)

    def applySCNMatrixToPoint(self, x, y):
        point_coords = numpy.array([x, y, 1])
        final_coords = numpy.matmul(point_coords, self.window_scn)
        return final_coords[0], final_coords[1]

