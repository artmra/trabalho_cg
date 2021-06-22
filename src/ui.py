from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QGridLayout, QVBoxLayout, QComboBox, QHBoxLayout
from viewport import Viewport


class Ui(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(1110, 810)
        self.setWindowTitle('T1 - Arthur Moreira R Alves & Bryan Martins Lima')
        # TODO: colocar icone pra ficar bonito
        self.setWindowIcon(QIcon('images/mainWindowIcon.png'))
        # TODO: colocar pra abrir no centro da tela
        self.createInnerLayout()
        self.show()

    # metodo responsável por criar o layout interno da janela
    def createInnerLayout(self) -> QWidget:
        # adiciona os componentes à janela principal
        funcMenu = createFuncMenu()
        funcMenu.setParent(self)
        funcMenu.move(5, 5)
        viewport = Viewport()
        viewport.setParent(self)
        viewport.move(305, 5)


    # TODO: Criar menu que mostra os objs
    # TODO: Criar menu que cria objs
    # TODO: Criar menu que deleta objs
    # TODO: Criar menu que edita objs
    # TODO: Criar viewport
    # TODO: implementar funcionalidade de zoom in/out
    # TODO: implementar funcionalidade de mover esq/dir/cima/baixo
    # TODO: implementar a transformada lá


# função responsável por criar o menu que contém as funcionalidades da aplicação
def createFuncMenu() -> QWidget:
    funcMenu = QWidget()
    funcMenu.setFixedSize(300, 800)
    layout = QVBoxLayout()
    objsMenu = createObjsMenu()
    objsMenu.setParent(funcMenu)
    layout.addWidget(objsMenu)
    movMenu = createMovementMenu()
    movMenu.setParent(funcMenu)
    layout.addWidget(movMenu)
    zoomMenu = createZoomMenu()
    zoomMenu.setParent(funcMenu)
    layout.addWidget(zoomMenu)
    funcMenu.setLayout(layout)
    return funcMenu


# função responsável por criar o menu que contém as funcionalidades de movimentação no viewport
def createMovementMenu() -> QWidget:
    movMenu = QWidget()
    movMenu.setFixedSize(250, 200)
    layout = QGridLayout()
    label = QLabel('Movimentação')
    label.setAlignment(QtCore.Qt.AlignCenter)
    layout.addWidget(label, 0, 0, 1, 3)
    layout.addWidget(QPushButton('Up'), 1, 1)
    layout.addWidget(QPushButton('Left'), 2, 0)
    layout.addWidget(QPushButton('Right'), 2, 2)
    layout.addWidget(QPushButton('Down'), 3, 1)
    movMenu.setLayout(layout)
    return movMenu


# função responsável por criar o menu de zoom in/out
def createZoomMenu() -> QWidget:
    zoomMenu = QWidget()
    zoomMenu.setFixedSize(250, 200)
    layout = QGridLayout()
    label = QLabel('Zoom')
    label.setAlignment(QtCore.Qt.AlignCenter)
    layout.addWidget(label, 0, 0, 1, 2)
    layout.addWidget(QPushButton('in'), 1, 0)
    layout.addWidget(QPushButton('out'), 1, 1)
    zoomMenu.setLayout(layout)
    return zoomMenu


# função responsável por criar o menu de objs
def createObjsMenu() -> QWidget:
    objsMenu = QWidget()
    objsMenu.setFixedSize(250, 200)
    layout = QGridLayout()
    label = QLabel('Viewport Elements')
    label.setAlignment(QtCore.Qt.AlignCenter)
    layout.addWidget(label, 0, 0, 1, 3)
    layout.addWidget(QComboBox(), 1, 0, 1, 2)
    layout.addWidget(QPushButton('+'), 1, 3)
    objsMenu.setLayout(layout)
    return objsMenu
