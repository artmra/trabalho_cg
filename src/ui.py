from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton, QGridLayout, QVBoxLayout, QComboBox, QGroupBox, QMainWindow

from src.createMenus import CreatePointMenu, CreateLineMenu, CreateWireframeMenu
from src.world import World
from viewport import Viewport


class Ui(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(1110, 810)
        self.setWindowTitle('T1 - Arthur Moreira R Alves & Bryan M Lima')
        self.setWindowIcon(QIcon('images/mainWindowIcon.png'))
        # world
        self.world = World()
        # viewport
        self.viewport = Viewport(self.world)
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
        upButton = QPushButton('Up')
        upButton.clicked.connect(self.clickMoveUp)
        layout.addWidget(upButton, 1, 1)
        leftButton = QPushButton('Left')
        leftButton.clicked.connect(self.clickMoveLeft)
        layout.addWidget(leftButton, 2, 0)
        rightButton = QPushButton('Right')
        rightButton.clicked.connect(self.clickMoveRight)
        layout.addWidget(rightButton, 2, 2)
        downButton = QPushButton('Down')
        downButton.clicked.connect(self.clickMoveDown)
        layout.addWidget(downButton, 3, 1)
        movMenu.setLayout(layout)
        return movMenu

    # função responsável por criar o menu de zoom in/out
    def createZoomMenu(self) -> QGroupBox:
        zoomMenu = QGroupBox('Zoom')
        zoomMenu.setFixedSize(250, 200)
        layout = QGridLayout()
        zoomInButton = QPushButton('in')
        zoomInButton.clicked.connect(self.clickZoomIn)
        layout.addWidget(zoomInButton, 1, 0)
        zoomOutButton = QPushButton('out')
        zoomOutButton.clicked.connect(self.clickZoomOut)
        layout.addWidget(zoomOutButton, 1, 1)
        zoomMenu.setLayout(layout)
        return zoomMenu

    # função responsável por criar o menu de objs
    def createObjsMenu(self) -> QGroupBox:
        objsMenu = QGroupBox('Objetos')
        objsMenu.setFixedSize(250, 200)
        layout = QGridLayout()
        self.objListView = QComboBox()
        layout.addWidget(self.objListView, 0, 0)
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

    # FUNCIONALIDADES DA APLICAÇÃO
    def clickCreatePoint(self):
        self.poinMenu = CreatePointMenu(self.viewport, self.objListView)
        self.poinMenu.show()

    def clickCreateLine(self):
        self.lineMenu = CreateLineMenu(self.viewport, self.objListView)
        self.lineMenu.show()

    def clickCreatePolygon(self):
        self.wireframeMenu = CreateWireframeMenu(self.viewport, self.objListView)
        self.wireframeMenu.show()

    def clickZoomIn(self):
        self.viewport.zoomIn()

    def clickZoomOut(self):
        self.viewport.zoomOut()

    def clickMoveUp(self):
        self.viewport.moveUp()

    def clickMoveLeft(self):
        self.viewport.moveLeft()

    def clickMoveRight(self):
        self.viewport.moveRight()

    def clickMoveDown(self):
        self.viewport.moveDown()
