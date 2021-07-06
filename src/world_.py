from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QPen
from PyQt5.QtWidgets import QGraphicsScene


# Classe que implementa o que corresponderia ao mundo da nossa aplicação, onde serão armazenados diversos obj 2D
from src.objs import TwoDObj
from src.window import Window


class World:
    def __init__(self):
        # Lista de objs 2D do mundo
        self.objs = list()
        self.window = Window(self)

    def getWindow(self) -> Window:
        return self.window

    def getObjs(self) -> list:
        # retorna todos os objs
        return self.objs

    def getObj(self, name: str) -> TwoDObj:
        # retorna um obj de attr name equivalente
        try:
            return [obj for obj in self.objs if obj.name == name][0]
        except Exception:
            raise Exception('Não há nenhum objeto com esse nome.')

    def updateObj(self, updatedObj: TwoDObj):
        # como o método de __eq__ dos objetos considera objetos com o mesmo nome iguais é possível atualizar o obj dessa
        # maneira
        self.objs = [updatedObj if updatedObj == obj else obj for obj in self.objs]

    def deleteObj(self, objToDelete: TwoDObj):
        # como o método de __eq__ dos objetos considera objetos com o mesmo nome iguais é possível deletar
        # um abj dessa maneira
        self.objs = [obj for obj in self.objs if obj != objToDelete]
        # listOfLines = self.qGraphicsObjs.pop(objToDelete)
        # for qGraphicsItem in listOfLines:
        #     self.removeItem(qGraphicsItem)

    # def getWorlCoords(self) -> (float, float, float, float):
    #     # coords = self.sceneRect().getCoords()
    #     # xwmin = coords[0]
    #     # ywmin = coords[1]
    #     # xwmax = coords[2]
    #     # ywmax = coords[3]
    #     return self.sceneRect().getCoords()
