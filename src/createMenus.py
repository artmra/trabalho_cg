from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QMessageBox

from src.objs import Point, Line


class CreateMenu(QWidget):
    def __init__(self, name, viewport):
        super().__init__()
        self.setWindowTitle(name)
        self.viewport = viewport
        self.createButton = QPushButton('Criar')
        self.cancelButton = QPushButton('Cancelar')
        self.cancelButton.clicked.connect(self.close)


class CreatePointMenu(CreateMenu):
    def __init__(self, viewport):
        super().__init__('Criação de Ponto', viewport)
        self.createButton.clicked.connect(self.clickCreate)
        layout = QGridLayout()
        self.x = QLineEdit()
        self.y = QLineEdit()
        self.name = QLineEdit()
        layout.addWidget(QLabel('Nome:'), 0, 0)
        layout.addWidget(self.name, 0, 1)
        layout.addWidget(QLabel('X:'), 1, 0)
        layout.addWidget(self.x, 1, 1)
        layout.addWidget(QLabel('Y:'), 2, 0)
        layout.addWidget(self.y, 2, 1)
        layout.addWidget(self.createButton, 3, 0)
        layout.addWidget(self.cancelButton, 3, 1)
        self.setLayout(layout)

    def clickCreate(self):
        try:
            obj = Point(self.name.text(), (self.x.text(), self.y.text()))
            if obj in self.viewport.scene().objs:
                msg = QMessageBox()
                msg.setWindowTitle('Erro no processo de criação')
                msg.setText('Não é possível criar objetos com o mesmo nome ou informações parecidas.')
                x = msg.exec_()
            else:
                self.viewport.createObj(obj)
                self.close()
        except Exception as e:
            msg = QMessageBox()
            msg.setWindowTitle('Erro no processo de criação')
            msg.setText(str(e))
            x = msg.exec_()


class CreateLineMenu(CreateMenu):
    def __init__(self, viewport):
        super().__init__('Criação de Linha', viewport)
        # self.setFixedSize(200, 200)
        self.createButton.clicked.connect(self.clickCreate)
        layout = QGridLayout()
        self.x1 = QLineEdit()
        self.y1 = QLineEdit()
        self.x2 = QLineEdit()
        self.y2 = QLineEdit()
        self.name = QLineEdit()
        layout.addWidget(QLabel('Nome:'), 0, 0, 1, 2)
        layout.addWidget(self.name, 0, 3, 1, 2)
        layout.addWidget(QLabel('X1:'), 1, 0)
        layout.addWidget(self.x1, 1, 1)
        layout.addWidget(QLabel('Y1:'), 1, 2)
        layout.addWidget(self.y1, 1, 3)
        layout.addWidget(QLabel('X2:'), 2, 0)
        layout.addWidget(self.x2, 2, 1)
        layout.addWidget(QLabel('Y2:'), 2, 2)
        layout.addWidget(self.y2, 2, 3)
        layout.addWidget(self.createButton, 3, 0, 1, 2)
        layout.addWidget(self.cancelButton, 3, 3, 1, 2)
        self.setLayout(layout)

    def clickCreate(self):
        try:
            obj = Line(self.name.text(), [(self.x1.text(), self.y1.text()), (self.x2.text(), self.y2.text())])
            if obj in self.viewport.scene().objs:
                msg = QMessageBox()
                msg.setWindowTitle('Erro no processo de criação')
                msg.setText('Não é possível criar objetos com o mesmo nome ou informações parecidas.')
                x = msg.exec_()
            else:
                self.viewport.createObj(obj)
                self.close()
        except Exception as e:
            msg = QMessageBox()
            msg.setWindowTitle('Erro no processo de criação')
            msg.setText(str(e))
            x = msg.exec_()


class CreatePolygonMenu(CreateMenu):
    def __init__(self, viewport):
        super().__init__('Criação de Poligono', viewport)
        layout = QGridLayout()
        self.label = QLabel("Another window damnit")
        layout.addWidget(self.label)
        self.setLayout(layout)
