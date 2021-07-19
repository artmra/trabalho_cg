import numpy


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
        # define o centro original da window(attr q pode ser usado para trazer a view de volta ao seu centro original)
        self.center = self.calcCenter()
        # define o novo centro(var que pode ser utilizada em futuros calculos envolvendo o centro da window)
        self.newCenter = self.center
        self.fatorMovimento = 10
        # TODO: definir uma representacao da window como obj 2d(wireframe) afim de utilizar os metodos de translacao, rotacao e "escalonamento" ja definidos.

    def calcCenter(self) -> tuple:
        return ((self.xyw_min[0] + self.xyw_max[0]) / 2, (self.xyw_min[1] + self.xyw_max[1]) / 2)

    def getCoords(self) -> tuple:
        return self.xyw_min[0], self.xyw_min[1], self.xyw_max[0], self.xyw_max[1]

    def moveUp(self):
        self._translate(dy=self.fatorMovimento)
        self.newCenter = self.calcCenter()

    def moveDown(self):
        self._translate(dy=(-1)*self.fatorMovimento)
        self.newCenter = self.calcCenter()

    def moveRight(self):
        self._translate(dx=self.fatorMovimento)
        self.newCenter = self.calcCenter()

    def moveLeft(self):
        self._translate(dx=(-1)*self.fatorMovimento)
        self.newCenter = self.calcCenter()

    def _translate(self, dx=0, dy=0):
        window_coords = numpy.array([[self.xyw_min[0], self.xyw_min[1], 1],
                                    [self.xyw_max[0], self.xyw_max[1], 1]])
        translate_matrix = numpy.array([[1, 0, 0], [0, 1, 0], [dx, dy, 1]])
        xyw_min, xyw_max = numpy.matmul(window_coords, translate_matrix)
        self.xyw_min = (xyw_min[0], xyw_min[1])
        self.xyw_max = (xyw_max[0], xyw_max[1])

    def zoomIn(self):
        self._scale(scale=0.9)
        self.fatorMovimento = self.fatorMovimento * 0.9
        self.newCenter = self.calcCenter()

    def zoomOut(self):
        self._scale(scale=1.1)
        self.fatorMovimento = self.fatorMovimento * 1.1
        self.newCenter = self.calcCenter()

    # escala um obj
    def _scale(self, scale=1):
        # centro do obj
        cx, cy = self.center
        # coords do mundo
        window_coords = numpy.array([[self.xyw_min[0], self.xyw_min[1], 1],
                                     [self.xyw_max[0], self.xyw_max[1], 1]])
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
        xyw_min, xyw_max = numpy.matmul(window_coords, transformations)
        # atualiza xyw_min/max
        self.xyw_min = (xyw_min[0], xyw_min[1])
        self.xyw_max = (xyw_max[0], xyw_max[1])
