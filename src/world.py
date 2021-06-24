from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QPen
from PyQt5.QtWidgets import QGraphicsScene


# Classe que implementa o que corresponderia ao mundo da nossa aplicação, onde serão armazenados diversos obj 2D
from src.objs import TwoDObj


class World(QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.setBackgroundBrush(QBrush(Qt.white))
        self.setSceneRect(0,0,800,800)
        self.addRect(self.sceneRect(), QPen(Qt.NoPen), QBrush(Qt.black))
        # Lista de objs 2D do mundo
        self.objs = list()

    def getObjs(self):
        return self.objs

    def getObj(self, objToGet) -> TwoDObj:
        try:
            return [obj for obj in self.objs if obj == objToGet][0]
        except Exception:
            raise Exception('Não há nenhum objeto com esse nome.')

    def updateObj(self, updatedObj):
        # como o método de __eq__ dos objetos considera objetos com o mesmo nome iguais é possível atualizar o obj dessa
        # maneira
        self.objs = [updatedObj if updatedObj == obj else obj for obj in self.objs]

    def deleteObj(self, objToDelete):
        # como o método de __eq__ dos objetos considera objetos com o mesmo nome iguais é possível deletar
        # um abj dessa maneira
        self.objs = [obj for obj in self.objs if obj != objToDelete]

    def getWorlCoords(self) -> (float, float, float, float):
        # coords = self.sceneRect().getCoords()
        # xwmin = coords[0]
        # ywmin = coords[1]
        # xwmax = coords[2]
        # ywmax = coords[3]
        return self.sceneRect().getCoords()


