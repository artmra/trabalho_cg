import numpy
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QPushButton, QGridLayout, QVBoxLayout, QComboBox, QGroupBox, QMainWindow

from createMenus import CreatePointMenu, CreateLineMenu, CreateWireframeMenu
from objs import Line, Point, Wireframe
from src.objs import TwoDObj
from world_ import World
from viewport_ import Viewport


class Ui(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(1110, 810)
        self.setWindowTitle('T1 - Arthur Moreira R Alves & Bryan M Lima')
        self.setWindowIcon(QIcon('images/uiIcon.png'))
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
        upButton = QPushButton()
        upButton.setStyleSheet('border: none')
        upButton.setIcon(QIcon(QPixmap('images/up.svg')))
        upButton.clicked.connect(self.clickMoveUp)
        layout.addWidget(upButton, 1, 1)
        leftButton = QPushButton()
        leftButton.setStyleSheet('border: none')
        leftButton.setIcon(QIcon(QPixmap('images/left.svg')))
        leftButton.clicked.connect(self.clickMoveLeft)
        layout.addWidget(leftButton, 2, 0)
        rightButton = QPushButton()
        rightButton.setStyleSheet('border: none')
        rightButton.setIcon(QIcon(QPixmap('images/right.svg')))
        rightButton.clicked.connect(self.clickMoveRight)
        layout.addWidget(rightButton, 2, 2)
        downButton = QPushButton()
        downButton.setStyleSheet('border: none')
        downButton.setIcon(QIcon(QPixmap('images/down.svg')))
        downButton.clicked.connect(self.clickMoveDown)
        layout.addWidget(downButton, 3, 1)
        movMenu.setLayout(layout)
        return movMenu

    # função responsável por criar o menu de zoom in/out
    def createZoomMenu(self) -> QGroupBox:
        zoomMenu = QGroupBox('Zoom')
        zoomMenu.setFixedSize(250, 200)
        layout = QGridLayout()
        zoomInButton = QPushButton()
        zoomInButton.setStyleSheet('border: none')
        zoomInButton.setIcon(QIcon(QPixmap('images/zoomin.svg')))
        zoomInButton.clicked.connect(self.clickZoomIn)
        layout.addWidget(zoomInButton, 1, 0)
        zoomOutButton = QPushButton()
        zoomOutButton.setStyleSheet('border: none')
        zoomOutButton.setIcon(QIcon(QPixmap('images/zoomout.svg')))
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
        self.objListView.setStyleSheet('border: none')
        layout.addWidget(self.objListView, 0, 0)
        # botao adicionar ponto
        addPointButton = QPushButton('Ponto')
        addPointButton.setStyleSheet('border: none')
        addPointButton.setIcon(QIcon(QPixmap('images/draw.svg')))
        # associa o metodo ao clique do botao
        addPointButton.clicked.connect(self.clickCreatePoint)
        layout.addWidget(addPointButton, 0, 1)
        # botao adicionar reta
        addLineButton = QPushButton('Linha')
        addLineButton.setStyleSheet('border: none')
        addLineButton.setIcon(QIcon(QPixmap('images/draw.svg')))
        addLineButton.clicked.connect(self.clickCreateLine)
        layout.addWidget(addLineButton, 1, 1)
        # botao adicionar poligono
        addPolyButton = QPushButton('Poligono')
        addPolyButton.setStyleSheet('border: none')
        addPolyButton.setIcon(QIcon(QPixmap('images/draw.svg')))
        addPolyButton.clicked.connect(self.clickCreatePolygon)
        layout.addWidget(addPolyButton, 2, 1)
        # botao pra deletar obj
        delObjButton = QPushButton('')
        delObjButton.setStyleSheet('border: none')
        delObjButton.setIcon(QIcon(QPixmap('images/delete.svg')))
        delObjButton.clicked.connect(self.clickDelOjb)
        layout.addWidget(delObjButton, 1, 0)
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

    def clickDelOjb(self):
        selectedItemName = self.objListView.currentText()
        self.viewport.deleteObj(selectedItemName)
        index = self.objListView.currentIndex()
        self.objListView.removeItem(index)

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

    # TODO TRANSFORM FINAL,Aqui sera enviado a matrix completa, com rotação escalonamento e translação
    def _transform(self, points, matrix):
        print("Hello")

    def _translate(self, obj: TwoDObj, points, matrix):
        # TODO get objeto
        self.objListView.currentText()
        dx = 0
        dy = 0
        trans_mat = numpy.array([[1, 0, 0], [0, 1, 0], [dx, dy, 1]])

        if isinstance(obj, Point):
            x = obj.getX()
            y = obj.getY()
            x_y = numpy.array([[x, y, 1]])
            new_x_y = numpy.matmul(x_y, trans_mat)
        #     TODO atualizar obj com as coordenadas
        elif isinstance(obj, Line):
            x1 = obj.getX1_Y1().index(0)
            y1 = obj.getX1_Y1().index(1)
            x2 = obj.getX2_Y2().index(0)
            y2 = obj.getX2_Y2().index(1)
            x_y1 = numpy.array([[x1, y1, 1]])
            x_y2 = numpy.array([[x2, y2, 1]])

            new_x1_y1 = numpy.matmul(x_y1, trans_mat)
            new_x1_y1 = numpy.matmul(x_y2, trans_mat)
        #     TODO atualizar obj
        elif isinstance(obj, Wireframe):
            result = list()
            for x_y in obj.getCoords():
                x = x_y.index(0)
                y = x_y.index(1)
                matrix = numpy.array([[x, y, 1]])
                result.append(numpy.matmul(matrix, trans_mat))
        #     TODO atualizar obj

    # TODO Determinar centro do objeto rotacionar e voltar a posicao original
    def _rotate(self, obj: TwoDObj, angle, matrix):
        deslo_mat1 = numpy.array([[1, 0, 0], [0, 1, 0], [dx, dy, 1]])
        rotate_mat = numpy.array([[1, 0, 0], [0, 1, 0], [dx, dy, 1]])
        deslo_mat2 = numpy.array([[1, 0, 0], [0, 1, 0], [dx, dy, 1]])

        # x, y = obj.getCenter()

        print("hello")

    # TODO Determinar centro do objeto escalonar e voltar a posicao original
    def _scale(self, obj: TwoDObj, scale_x, scale_y, matrix):
        cx, cy = obj.getCenter()
        deslo_mat1 = numpy.array([[1, 0, 0], [0, 1, 0], [cx, cy, 1]])
        scale_mat = numpy.array([[scale_x, 0, 0], [0, scale_y, 0], [0, 0, 1]])
        deslo_mat2 = numpy.array([[1, 0, 0], [0, 1, 0], [cx, cy, 1]])


        print("hello")
