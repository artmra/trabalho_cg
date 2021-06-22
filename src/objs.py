from enum import Enum


# Enum para tipos de objs 2D
class TwoDObjType(Enum):
    POINT = 0
    LINE = 1
    POLY = 2


# Esquema padrão de todos os objs 2D
class TwoDObj:
    def __init__(self, name, type):
        self.name = name
        self.type = TwoDObjType(type)
        self.coords = list()

    def getName(self) -> str: return self.name

    def getType(self) -> TwoDObjType: return self.type

    def getCoords(self) -> list: return self.coords


# Classe que representa um ponto
class Point(TwoDObj):
    def __init__(self, name, x_y=(0, 0)):
        super().__init__(name, 0)
        # TODO: checar se as tuplas são compostas de números?
        if x_y is not tuple or len(x_y) != 2:
            raise Exception('O param x_y deve ser uma tupla de 2 valores.')
        self.coords.append(x_y)
        self.x = x_y[0]
        self.y = x_y[1]

    def getX(self): return self.x

    def getY(self): return self.y


# Classe que representa uma linha
class Line(TwoDObj):
    def __init__(self, name, coords=[(0, 0), (1, 1)]):
        super().__init__(name, 1)
        # TODO: checar se as tuplas são compostas de números?
        for x_y in coords:
            if x_y is not tuple or len(x_y) != 2:
                raise Exception('A lista de coordenadas deve conter apenas tuplas de dois valores.')
        self.coords.extend(coords)
        try:
            self.x1_y1, self.x2_y2 = coords
        except:
            raise Exception('Devem haver apenas 2 tuplas: a 1ª será (x1, y1) e a 2ª (x2, y2).')

    def getX1_Y1(self) -> tuple:
        return self.x1_y1

    def getX2_Y2(self) -> tuple:
        return self.x2_y2


# Classe que representa um polígono
class Polygon(TwoDObj):
    def __init__(self, name, coords=[(0, 0), (1, 1), (0, 2)]):
        super().__init__(name, 2)
        # TODO: checar se as tuplas são compostas de números?
        for x_y in coords:
            if x_y is not tuple or len(x_y) != 2:
                raise Exception('A lista de coordenadas deve conter apenas tuplas de dois valores.')
        self.coords.extend(coords)
