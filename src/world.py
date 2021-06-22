from PyQt5.QtWidgets import QGraphicsScene


# Classe que implementa o que corresponderia ao mundo da nossa aplicação, onde serão armazenados diversos obj 2D
class World(QGraphicsScene):
    def __init__(self):
        super().__init__()
        # Lista de objs 2D do mundo
        self.objs = list()

    def getObjs(self): return self.objs


