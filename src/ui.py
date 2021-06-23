from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton, QGridLayout, QVBoxLayout, QComboBox, QGroupBox, QMainWindow

from src.createMenus import CreatePointMenu, CreateLineMenu, CreatePolygonMenu
from viewport import Viewport


class Ui(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(1110, 810)
        self.setWindowTitle('T1 - Arthur Moreira R Alves & Bryan M Lima')
        self.setWindowIcon(QIcon('images/mainWindowIcon.png'))
        # viewport
        self.viewport = Viewport()
        self.viewport.setParent(self)
        self.viewport.move(305, 5)
        # menu com as funcionalidades da aplicação
        self.funcMenu = self.createFuncMenu()
        self.funcMenu.setParent(self)
        self.funcMenu.move(5, 5)

    # função responsável por criar o menu que contém as funcionalidades da aplicação
    def createFuncMenu(self) -> QGroupBox:
        funcMenu = QGroupBox()
        funcMenu.setFixedSize(300, 800)
        layout = QVBoxLayout()
        objsMenu = self.createObjsMenu()
        objsMenu.setParent(funcMenu)
        layout.addWidget(objsMenu)
        movMenu = self.createMovementMenu()
        movMenu.setParent(funcMenu)
        layout.addWidget(movMenu)
        zoomMenu = self.createZoomMenu()
        zoomMenu.setParent(funcMenu)
        layout.addWidget(zoomMenu)
        funcMenu.setLayout(layout)

        return funcMenu

    # função responsável por criar o menu que contém as funcionalidades de movimentação no viewport
    def createMovementMenu(self) -> QGroupBox:
        movMenu = QGroupBox('Movimentação')
        movMenu.setFixedSize(250, 200)
        layout = QGridLayout()
        layout.addWidget(QPushButton('Up'), 1, 1)
        layout.addWidget(QPushButton('Left'), 2, 0)
        layout.addWidget(QPushButton('Right'), 2, 2)
        layout.addWidget(QPushButton('Down'), 3, 1)
        movMenu.setLayout(layout)
        return movMenu

    # função responsável por criar o menu de zoom in/out
    def createZoomMenu(self) -> QGroupBox:
        zoomMenu = QGroupBox('Zoom')
        zoomMenu.setFixedSize(250, 200)
        layout = QGridLayout()
        layout.addWidget(QPushButton('in'), 1, 0)
        layout.addWidget(QPushButton('out'), 1, 1)
        zoomMenu.setLayout(layout)
        return zoomMenu

    # função responsável por criar o menu de objs
    def createObjsMenu(self) -> QGroupBox:
        objsMenu = QGroupBox('Objetos')
        objsMenu.setFixedSize(250, 200)
        layout = QGridLayout()
        layout.addWidget(QComboBox(), 0, 0)
        # botao adicionar ponto
        addPointButton = QPushButton('+ Ponto')
        # associa o metodo ao clique do botao
        addPointButton.clicked.connect(self.clickCreatePoint)
        layout.addWidget(addPointButton, 0, 1)
        # botao adicionar reta
        addLineButton = QPushButton('+ Linha')
        addLineButton.clicked.connect(self.clickCreateLine)
        layout.addWidget(addLineButton, 1, 1)
        # botao adicionar poligono
        addPolyButton = QPushButton('+ Poligono')
        addPolyButton.clicked.connect(self.clickCreatePolygon)
        layout.addWidget(addPolyButton, 2, 1)
        objsMenu.setLayout(layout)
        return objsMenu

    # MÉTODOS DA APLICAÇÃO
    def clickCreatePoint(self):
        self.createPoinMenu = CreatePointMenu(self.viewport)
        self.createPoinMenu.show()

    def clickCreateLine(self):
        self.createLineMenu = CreateLineMenu(self.viewport)
        self.createLineMenu.show()

    def clickCreatePolygon(self):
        self.createPolygonMenu = CreatePolygonMenu(self.viewport)
        self.createPolygonMenu.show()

    # TODO: Criar menu que mostra os objs
    # TODO: Criar menu que cria objs
    # TODO: Criar menu que deleta objs
    # TODO: Criar menu que edita objs
    # TODO: Criar viewport
    # TODO: implementar funcionalidade de zoom in/out
    # TODO: implementar funcionalidade de mover esq/dir/cima/baixo
    # TODO: implementar a transformada lá
