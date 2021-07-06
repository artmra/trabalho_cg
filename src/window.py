
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

    def calcCenter(self) -> tuple:
        return ((self.xyw_min[0] + self.xyw_max[0]) / 2, (self.xyw_min[1] + self.xyw_max[1]) / 2)

    def getCoords(self) -> tuple:
        return self.xyw_min[0], self.xyw_min[1], self.xyw_max[0], self.xyw_max[1]

    def moveUp(self):
        self.xyw_min = (self.xyw_min[0], self.xyw_min[1] + 5)
        self.xyw_max = (self.xyw_max[0], self.xyw_max[1] + 5)
        self.newCenter = self.calcCenter()

    def moveDown(self):
        self.xyw_min = (self.xyw_min[0], self.xyw_min[1] - 5)
        self.xyw_max = (self.xyw_max[0], self.xyw_max[1] - 5)
        self.newCenter = self.calcCenter()

    def moveRight(self):
        self.xyw_min = (self.xyw_min[0] + 5, self.xyw_min[1])
        self.xyw_max = (self.xyw_max[0] + 5, self.xyw_max[1])
        self.newCenter = self.calcCenter()

    def moveLeft(self):
        self.xyw_min = (self.xyw_min[0] - 5, self.xyw_min[1])
        self.xyw_max = (self.xyw_max[0] - 5, self.xyw_max[1])
        self.newCenter = self.calcCenter()

    def zoomIn(self):
        self.xyw_min = (self.xyw_min[0] - 5, self.xyw_min[1] - 5)
        self.xyw_max = (self.xyw_max[0] - 5, self.xyw_max[1] - 5)
        self.newCenter = self.calcCenter()

    def zoomOut(self):
        self.xyw_min = (self.xyw_min[0] + 5, self.xyw_min[1] + 5)
        self.xyw_max = (self.xyw_max[0] + 5, self.xyw_max[1] + 5)
        self.newCenter = self.calcCenter()
