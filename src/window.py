from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QGridLayout, QVBoxLayout


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(1000,800)
        self.setWindowTitle('Trabalho CG - Arthur Moreira R Alves & Bryan Martins Lima')
        # TODO: colocar icone pra ficar bonito
        # TODO: colocar pra abrir no centro da tela


        # adiciona os componentes à janela principal
        layout = QGridLayout()
        funcMenu = self.createFuncMenu()
        funcMenu.setParent(self)
        layout.addWidget(funcMenu, 0, 0)
        self.show()


    # metodo responsável por criar o menu que contém as funcionalidades da aplicação
    def createFuncMenu(self) -> QWidget:
        funcMenu = QWidget()
        layout = QVBoxLayout()
        movMenu = self.createMovementMenu()
        movMenu.setParent(funcMenu)
        layout.addWidget(movMenu)
        funcMenu.setLayout(layout)
        return funcMenu

    # metodo responsável por criar o menu que contém as funcionalidades de movimentação no viewport
    def createMovementMenu(self) -> QWidget:
        movMenu = QWidget()
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

    # TODO: Criar menu de zoon in/ zoon out
    # TODO: Criar menu que mostra os objs
    # TODO: Criar menu que cria objs
    # TODO: Criar menu que deleta objs
    # TODO: Criar menu que edita objs
    # TODO: Criar viewport
    # TODO: implementar funcionalidade de zoom in/out
    # TODO: implementar funcionalidade de mover esq/dir/cima/baixo
    # TODO: implementar a transformada lá