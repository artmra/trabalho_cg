from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtCore import Qt
import random
from world import World


# Classe que implementa uma viewport para a aplicação
class Viewport(QGraphicsView):

    def __init__(self, world):
        super().__init__()
        self.setFixedSize(800, 800)
        self.setScene(world)

    def createObj(self, obj):
        self.scene().objs.append(obj)

    def drawPoints(self, qp):
        qp.setPen(Qt.red)
        size = self.size()

        if size.height() <= 1 or size.height() <= 1:
            return

        for i in range(1000):
            x = random.randint(1, size.width() - 1)
            y = random.randint(1, size.height() - 1)
            qp.drawPoint(x, y)
