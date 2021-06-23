from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel


class CreatePointMenu(QWidget):
    def __init__(self, viewport):
        super().__init__()
        self.setWindowTitle('Criação de Ponto')
        self.setFixedSize(500, 500)
        layout = QGridLayout()
        self.label = QLabel("Another window damnit")
        layout.addWidget(self.label)
        self.setLayout(layout)


class CreateLineMenu(QWidget):
    def __init__(self, viewport):
        QWidget.__init__(self)
        self.setWindowTitle('Criação de Ponto')
        self.setFixedSize(500, 500)
        layout = QGridLayout()
        self.label = QLabel("Another window damnit")
        layout.addWidget(self.label)
        self.setLayout(layout)


class CreatePolygonMenu(QWidget):
    def __init__(self, viewport):
        QWidget.__init__(self)
        self.setWindowTitle('Criação de Polígono')
        self.setFixedSize(500, 500)
        layout = QGridLayout()
        self.label = QLabel("Another window damnit")
        layout.addWidget(self.label)
        self.setLayout(layout)
