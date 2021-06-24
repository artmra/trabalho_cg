from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox
from src.objs import Point, Line, Wireframe
from src.viewport import Viewport


# classe base com elementos comuns a todas as classes de criacao de obj
class CreateMenu(QWidget):
    def __init__(self, name, viewport: Viewport, objListView: QComboBox):
        super().__init__()
        self.setWindowTitle(name)
        self.viewport = viewport
        self.objListView = objListView
        self.createButton = QPushButton('Criar')
        self.createButton.setStyleSheet('border: none')
        self.cancelButton = QPushButton('Cancelar')
        self.cancelButton.setStyleSheet('border: none')
        self.cancelButton.clicked.connect(self.close)

# janela de criacao de pontos
class CreatePointMenu(CreateMenu):
    def __init__(self, viewport: Viewport, objListView: QComboBox):
        super().__init__('Criação de Ponto', viewport, objListView)
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
                self.viewport.addObj(obj)
                self.objListView.addItem(obj.name)
                self.viewport.drawPoint(obj)
                self.close()
        except Exception as e:
            msg = QMessageBox()
            msg.setWindowTitle('Erro no processo de criação')
            msg.setWindowIcon(QIcon('images/warning.svg'))
            msg.setText(str(e))
            x = msg.exec_()


# janela de criacao de pontos
class CreateLineMenu(CreateMenu):
    def __init__(self, viewport: Viewport, objListView: QComboBox):
        super().__init__('Criação de Linha', viewport, objListView)
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
                self.viewport.addObj(obj)
                self.objListView.addItem(obj.name)
                self.viewport.drawLine(obj)
                self.close()
        except Exception as e:
            msg = QMessageBox()
            msg.setWindowTitle('Erro no processo de criação')
            msg.setText(str(e))
            x = msg.exec_()


# janela de criacao de poligonos
class CreateWireframeMenu(CreateMenu):
    def __init__(self, viewport: Viewport, objListView: QComboBox, inputCoords=None):
        super().__init__('Criação de Linha', viewport, objListView)
        self.createButton.clicked.connect(self.clickCreate)
        self.addCoordButton = QPushButton()
        self.addCoordButton.setStyleSheet('border: none')
        self.addCoordButton.setIcon(QIcon(QPixmap('images/addCoord.svg')))
        self.inputCoords = [(QLineEdit(), QLineEdit()), (QLineEdit(), QLineEdit()), (QLineEdit(), QLineEdit())] if inputCoords is None else inputCoords
        self.loadLayout()
        self.addCoordButton.clicked.connect(self.updateLayout)

    def clickCreate(self):
        try:
            coords = [(xyin[0].text(), xyin[1].text()) for xyin in self.inputCoords]
            obj = Wireframe(self.name.text(), coords)
            if obj in self.viewport.scene().objs:
                msg = QMessageBox()
                msg.setWindowTitle('Erro no processo de criação')
                msg.setText('Não é possível criar objetos com o mesmo nome ou informações parecidas.')
                x = msg.exec_()
            else:
                self.viewport.addObj(obj)
                self.objListView.addItem(obj.name)
                self.viewport.drawWireframe(obj)
                self.close()
        except Exception as e:
            msg = QMessageBox()
            msg.setWindowTitle('Erro no processo de criação')
            msg.setText(str(e))
            x = msg.exec_()

    def updateLayout(self):
        self.close()
        self.inputCoords.append((QLineEdit(), QLineEdit()))
        self.wireframeMenu = CreateWireframeMenu(self.viewport, self.objListView, self.inputCoords)
        self.wireframeMenu.show()

    def loadLayout(self):
        layout = QGridLayout()
        self.name = QLineEdit()
        layout.addWidget(QLabel('Nome:'), 0, 0, 1, 2)
        layout.addWidget(self.name, 0, 3, 1, 2)
        for n in range(0, len(self.inputCoords)):
            xyInput = self.inputCoords[n]
            xInput = xyInput[0]
            yInput = xyInput[1]
            n_ = n + 1
            layout.addWidget(QLabel(f'X{n_}:'), n_, 0)
            layout.addWidget(xInput, n_, 1)
            layout.addWidget(QLabel(f'Y{n_}:'), n_, 2)
            layout.addWidget(yInput, n_, 3)
        layout.addWidget(self.addCoordButton, len(self.inputCoords) + 1, 0, 1, 4)
        layout.addWidget(self.createButton, len(self.inputCoords) + 2, 0, 1, 2)
        layout.addWidget(self.cancelButton, len(self.inputCoords) + 2, 3, 1, 2)
        self.setLayout(layout)
