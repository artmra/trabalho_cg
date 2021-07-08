from enum import Enum


# Enum para tipos de objs 2D
class TwoDObjType(Enum):
    POINT = 0
    LINE = 1
    POLY = 2


# Esquema padrão de todos os objs 2D
class TwoDObj:
    def __init__(self, name, twoDType):
        self.name = str(name)
        self.twoDType = TwoDObjType(twoDType)
        self.coords = list()

    def __eq__(self, other):
        # no contexto desse trabalho todos os objetos devem ter nomes diferentes, e caso sejam de tipos iguais n podem
        # ter coordenadas iguais. O teste deixa passar objetos iguais com coordenadas invertidas, algo que
        # será corrigido
        return other.name == self.name \
               or (isinstance(other, TwoDObj) and other.twoDType == self.twoDType and other.coords == self.coords)

    def __hash__(self):
        # implementada para permitir usar objs 2d como keys em dicts
        return hash((self.name, self.twoDType.value))

    def getName(self) -> str:
        return self.name

    def getType(self) -> TwoDObjType:
        return self.type

    def getCoords(self) -> list:
        return self.coords

    def getCenter(self):
        return self.coords


# Classe que representa um ponto
class Point(TwoDObj):
    def __init__(self, name, x_y=(0, 0)):
        super().__init__(name, 0)
        if not isinstance(x_y, tuple) or len(x_y) != 2:
            raise Exception('O param x_y deve ser uma tupla de 2 valores.')
        try:
            x_y = (float(x_y[0]), float(x_y[1]))
        except Exception:
            raise Exception('As coordenadas devem ser pares de números.')
        self.coords.append(x_y)
        self.x = float(x_y[0])
        self.y = float(x_y[1])

    def getX(self) -> float:
        return self.x

    def getY(self) -> float:
        return self.y

    def setX(self, x):
        self.x = float(x)

    def setY(self, y):
        self.y = float(y)


# Classe que representa uma linha
class Line(TwoDObj):
    def __init__(self, name, coords=[(0, 0), (1, 1)]):
        super().__init__(name, 1)
        try:
            x1_y1, x2_y2 = coords
        except:
            raise Exception('Devem haver apenas 2 tuplas: a 1ª será (x1, y1) e a 2ª (x2, y2).')

        for x_y in coords:
            if not isinstance(x_y, tuple) or len(x_y) != 2:
                raise Exception('A lista de coordenadas deve conter apenas tuplas de dois valores.')
            try:
                x_y = (float(x_y[0]), float(x_y[1]))
                self.coords.append(x_y)
            except Exception:
                raise Exception('As coordenadas devem ser pares de números.')
        self.x1_y1 = (float(x1_y1[0]), float(x1_y1[1]))
        self.x2_y2 = (float(x2_y2[0]), float(x2_y2[1]))

    def getX1_Y1(self) -> tuple:
        return self.x1_y1

    def getX2_Y2(self) -> tuple:
        return self.x2_y2

    def getCenter(self):
        x1 = self.getX1_Y1().index(0)
        y1 = self.getX1_Y1().index(1)
        x2 = self.getX2_Y2().index(0)
        y2 = self.getX2_Y2().index(1)
        return (x1+x2)/2, (y1+y2)/2


# Classe que representa um polígono
class Wireframe(TwoDObj):
    def __init__(self, name, coords=[(0, 0), (1, 1), (0, 2)]):
        super().__init__(name, 2)
        for x_y in coords:
            if not isinstance(x_y, tuple) or len(x_y) != 2:
                raise Exception('A lista de coordenadas deve conter apenas tuplas de dois valores.')
            try:
                x_y = (float(x_y[0]), float(x_y[1]))
                self.coords.append(x_y)
            except Exception:
                raise Exception('As coordenadas devem ser pares de números.')

    def getCenter(self):
        x = 0
        y = 0
        for x_y in self.coords:
            x += x_y.index(0)
            y += x_y.index(1)
        return (x/len(self.coords)), (y/len(self.coords))
