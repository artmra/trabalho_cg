from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
import random


class Viewport(QWidget):

    def __init__(self):
        super().__init__()
        self.setFixedSize(800, 800)
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.black)
        self.setPalette(p)

    # def paintEvent(self, e):
    #     qp = QPainter()
    #     qp.begin(self)
    #     self.drawPoints(qp)
    #     qp.end()

    def drawPoints(self, qp):
        qp.setPen(Qt.red)
        size = self.size()

        if size.height() <= 1 or size.height() <= 1:
            return

        for i in range(1000):
            x = random.randint(1, size.width() - 1)
            y = random.randint(1, size.height() - 1)
            qp.drawPoint(x, y)
