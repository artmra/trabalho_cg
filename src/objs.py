from enum import Enum
from PyQt5.QtGui import QColor


# Enum para tipos de objs 2D


class TwoDObjType(Enum):
    POINT = 0
    LINE = 1
    POLY = 2


# Esquema padrão de todos os objs 2D
class TwoDObj:
    def __init__(self, name, twoDType, color):
        self.name = str(name)
        self.twoDType = TwoDObjType(twoDType)
        self.coords = list()
        self.color = QColor(int(color[0]), int(color[1]), int(color[2]), 100)

    def __eq__(self, other):
        # no contexto desse trabalho todos os objetos devem ter nomes diferentes, e caso sejam de tipos iguais n podem
        # ter coordenadas iguais. O teste deixa passar objetos iguais com coordenadas invertidas, algo que
        # será corrigido
        return other.name == self.name \
               or (isinstance(other, TwoDObj) and other.twoDType == self.twoDType and other.coords == self.coords)

    def __hash__(self):
        # implementada para permitir usar objs 2d como keys em dicts
        return hash((self.name, self.twoDType.value))

    # TODO 3D set coord of z axis
    def objString(self):
        obj_string = list()
        for coord in self.coords:
            v_string = f'v {coord[0]} {coord[1]} 0.0'
            obj_string.append(v_string)
        return obj_string

    def getName(self) -> str:
        return self.name

    def getType(self) -> TwoDObjType:
        return self.type

    def getCoords(self) -> list:
        return self.coords

    def getColor(self) -> QColor:
        return self.color


# Classe que representa um ponto
class Point(TwoDObj):
    def __init__(self, name, x_y=(0, 0), color=(255, 0, 0)):
        super().__init__(name, 0, color)
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

    def getCenter(self):
        return self.x, self.y


# Classe que representa uma linha
class Line(TwoDObj):
    def __init__(self, name, coords=[(0, 0), (1, 1)], color=(0, 255, 0)):
        super().__init__(name, 1, color)
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
        x1 = self.getX1_Y1()[0]
        y1 = self.getX1_Y1()[1]
        x2 = self.getX2_Y2()[0]
        y2 = self.getX2_Y2()[1]
        return (x1 + x2) / 2, (y1 + y2) / 2


# Classe que representa um polígono
class Wireframe(TwoDObj):
    def __init__(self, name, coords=[(0, 0), (1, 1), (0, 2)], color=(204, 0, 204)):
        super().__init__(name, 2, color)
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
            x += x_y[0]
            y += x_y[1]
        return (x / len(self.coords)), (y / len(self.coords))


class DescritorOBJ:
    def __init__(self):
        self.count = 1
        self.coords = dict()
        self.mtls = dict()
        self.list_objs = list()

    def importObj(self, filename):
        try:
            with open(filename) as file:
                for line in file:
                    if line.startswith("v"):
                        coords = ''.join(line.split('v ', 1))
                        coord_list = list()
                        for coord in coords.split(" ", 2):
                            coord_list.append(float(coord))
                        self.coords[self.count] = coord_list
                        self.count += 1
                    elif line.startswith("mtllib"):
                        mtl_file = ''.join(line.split('mtllib ')).replace('\n', "")
                        mtl_file = filename.rsplit('/', 1)[0] + '/' + mtl_file
                        self.import_mtl(mtl_file)
                    elif line.startswith("o"):
                        obj_name = ''.join(line.split('o ')).replace('\n', "")
                        color = (255, 255, 0)  # Default color if doesnt specify in the file
                        next_line = next(file)
                        # Colors
                        if next_line.startswith("usemtl"):
                            mtl = ''.join(next_line.split('usemtl ')).replace('\n', "")
                            color = self.mtls[mtl]
                            next_line = next(file)
                        # Coords
                        x_y = list()
                        obj_coord = ''.join(next_line[2:]).replace('\n', "").split()
                        for point in obj_coord:
                            x = self.coords.get(int(point))[0]
                            y = self.coords.get(int(point))[1]
                            # TODO z axis here on 3D version
                            x_y.append((x, y))
                        if next_line.startswith("p"):
                            self.list_objs.append(Point(obj_name, x_y[0], color))
                        elif next_line.startswith("l"):
                            try:
                                self.list_objs.append(Line(obj_name, x_y, color))
                            except:
                                try:
                                    self.list_objs.append(Wireframe(obj_name, x_y, color))
                                except Exception as e:
                                    return e
        except Exception as e:
            return e

    def import_mtl(self, mtl_filename):
        try:
            with open(mtl_filename) as file:
                for line in file:
                    if line.startswith("newmtl"):
                        material_name = ''.join(line.split('newmtl ', 1)).replace('\n', "")
                        mtl_values = list()
                        rgb_values = next(file)
                        rgb_values = ''.join(rgb_values[2:]).replace('\n', "").split()
                        for value in rgb_values:
                            mtl_values.append(float(value)*255)
                        self.mtls[material_name] = mtl_values

        except Exception as e:
            return e

    def exportObj(self, world):
        vector_string = ""
        objs = ""

        for obj in world.objs:
            points = ""
            for coord in obj.objString():
                vector_string += coord + '\n'
                points += f' {self.count}'
                self.count += 1

            objs += f"o {obj.getName()}\n"
            if obj.getType == 0:
                objs += "p" + points + "\n"
            else:
                objs += "l" + points + "\n"

        return vector_string + objs
