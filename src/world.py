from PyQt5.QtWidgets import QGraphicsScene


# Classe que implementa o que corresponderia ao mundo da nossa aplicação, onde serão armazenados diversos obj 2D
class World(QGraphicsScene):
    def __init__(self):
        super().__init__()
        # Lista de objs 2D do mundo
        self.objs = list()

    def getObjs(self):
        return self.objs

    def getObj(self, name):
        try:
            return [obj for obj in self.objs if obj.name == name][0]
        except Exception:
            raise Exception('Não há nenhum objeto com esse nome.')


