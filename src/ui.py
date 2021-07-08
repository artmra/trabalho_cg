import numpy
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QPushButton, QGridLayout, QVBoxLayout, QComboBox, QGroupBox, QMainWindow, QLabel, \
    QMessageBox

from createMenus import CreatePointMenu, CreateLineMenu, CreateWireframeMenu, CreateTransformMenu
from objs import Line, Point, Wireframe
from src.objs import TwoDObj
from world import World
from viewport import Viewport
from world import World
from viewport import Viewport


class Ui(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(1110, 810)
        self.setWindowTitle('T1 - Arthur M R Alves & Bryan M Lima')
        self.setWindowIcon(QIcon('uiIcon.png'))
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
        funcMenu.setLayout(layout)
        return funcMenu

    # função responsável por criar o menu que contém as funcionalidades de movimentação da window
    def createMovementMenu(self) -> QGroupBox:
        movMenu = QGroupBox('Window')
        movMenu.setFixedSize(250, 200)
        layout = QGridLayout()
        layout.addWidget(QLabel('Movimentação'), 0, 0, 1, 3)
        upButton = QPushButton()
        upButton.setIcon(QIcon(QPixmap('up.svg')))
        upButton.clicked.connect(self.clickMoveUp)
        layout.addWidget(upButton, 1, 1, 1, 2)
        leftButton = QPushButton()
        leftButton.setIcon(QIcon(QPixmap('left.svg')))
        leftButton.clicked.connect(self.clickMoveLeft)
        layout.addWidget(leftButton, 2, 0, 1, 2)
        rightButton = QPushButton()
        rightButton.setIcon(QIcon(QPixmap('right.svg')))
        rightButton.clicked.connect(self.clickMoveRight)
        layout.addWidget(rightButton, 2, 2, 1, 2)
        downButton = QPushButton()
        downButton.setIcon(QIcon(QPixmap('down.svg')))
        downButton.clicked.connect(self.clickMoveDown)
        layout.addWidget(downButton, 3, 1, 1, 2)
        layout.addWidget(QLabel('Zoom'), 4, 0, 1, 3)
        zoomInButton = QPushButton()
        zoomInButton.setIcon(QIcon(QPixmap('zoomin.svg')))
        zoomInButton.clicked.connect(self.clickZoomIn)
        layout.addWidget(zoomInButton, 5, 0, 1, 2)
        zoomOutButton = QPushButton()
        zoomOutButton.setIcon(QIcon(QPixmap('zoomout.svg')))
        zoomOutButton.clicked.connect(self.clickZoomOut)
        layout.addWidget(zoomOutButton, 5, 2, 1, 2)

        movMenu.setLayout(layout)
        return movMenu

    # função responsável por criar o menu de zoom in/out
    def createZoomMenu(self) -> QGroupBox:
        zoomMenu = QGroupBox('Zoom')
        zoomMenu.setFixedSize(250, 200)
        layout = QGridLayout()
        zoomInButton = QPushButton()
        zoomInButton.setIcon(QIcon(QPixmap('zoomin.svg')))
        zoomInButton.clicked.connect(self.clickZoomIn)
        layout.addWidget(zoomInButton, 1, 0)
        zoomOutButton = QPushButton()
        zoomOutButton.setIcon(QIcon(QPixmap('zoomout.svg')))
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
        addPointButton = QPushButton('Ponto')
        addPointButton.setIcon(QIcon(QPixmap('draw.svg')))
        # associa o metodo ao clique do botao
        addPointButton.clicked.connect(self.clickCreatePoint)
        layout.addWidget(addPointButton, 0, 1)
        # botao adicionar reta
        addLineButton = QPushButton('Linha')
        addLineButton.setIcon(QIcon(QPixmap('draw.svg')))
        addLineButton.clicked.connect(self.clickCreateLine)
        layout.addWidget(addLineButton, 1, 1)
        # botao adicionar poligono
        addPolyButton = QPushButton('Poligono')
        addPolyButton.setIcon(QIcon(QPixmap('draw.svg')))
        addPolyButton.clicked.connect(self.clickCreatePolygon)
        layout.addWidget(addPolyButton, 2, 1)
        # botao pra deletar obj
        delObjButton = QPushButton('')
        delObjButton.setIcon(QIcon(QPixmap('delete.svg')))
        delObjButton.clicked.connect(self.clickDelOjb)
        layout.addWidget(delObjButton, 1, 0)
        # botao para transformação de obj
        addTransButton = QPushButton('Transformação')
        addTransButton.setIcon(QIcon(QPixmap('draw.svg')))
        addTransButton.clicked.connect(self.clickTransform)
        layout.addWidget(addTransButton, 2, 0)

        objsMenu.setLayout(layout)
        return objsMenu

    def clickCreatePoint(self):
        self.poinMenu = CreatePointMenu(self.viewport, self.objListView)
        self.poinMenu.show()

    def clickCreateLine(self):
        self.lineMenu = CreateLineMenu(self.viewport, self.objListView)
        self.lineMenu.show()

    def clickCreatePolygon(self):
        self.wireframeMenu = CreateWireframeMenu(self.viewport, self.objListView)
        self.wireframeMenu.show()

    def clickTransform(self):
        if self.objListView.currentIndex() == -1:
            msg = QMessageBox()
            msg.setWindowTitle('Não há o que transformar')
            msg.setText(str('A lista de objetos esta vazia.'))
            x = msg.exec_()
        else:
            self.transformMenu = CreateTransformMenu(self.viewport, self.objListView)
            self.transformMenu.translate_save_button.clicked.connect(self.click_translate)
            self.transformMenu.transformButton.clicked.connect(self.click_transform)
            self.transformMenu.show()

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

    def click_transform(self):
        trans_matrix = self.transformMenu.trans_matrix
        current_obj_name = self.objListView.currentText()
        obj = self.world.getObj(current_obj_name)

        if isinstance(obj, Point):
            x = obj.getX()
            y = obj.getY()
            x_y = numpy.array([x, y, 1])
            new_x, new_y, _ = numpy.matmul(x_y, trans_matrix)
            new_obj = Point(obj.name, (new_x, new_y))
            self.world.updateObj(new_obj)
            self.viewport.update()
            self.transformMenu.close()
        elif isinstance(obj, Line):
            x1 = obj.getX1_Y1()[0]
            y1 = obj.getX1_Y1()[1]
            x2 = obj.getX2_Y2()[0]
            y2 = obj.getX2_Y2()[1]
            x_y1 = numpy.array([x1, y1, 1])
            x_y2 = numpy.array([x2, y2, 1])

            new_x1, new_y1, _ = numpy.matmul(x_y1, trans_matrix)
            new_x2, new_y2, _ = numpy.matmul(x_y2, trans_matrix)

            new_obj = Line(obj.name, [(new_x1, new_y1), (new_x2, new_y2)])
            self.world.updateObj(new_obj)
            self.viewport.update()
            self.transformMenu.close()
        elif isinstance(obj, Wireframe):
            new_coords = list()
            for x_y in obj.getCoords():
                x = x_y[0]
                y = x_y[1]
                x_y = numpy.array([x, y, 1])

                new_x, new_y, _ = numpy.matmul(x_y, trans_matrix)
                new_coords.append((new_x, new_y))
            new_obj = Wireframe(obj.name, new_coords)
            self.world.updateObj(new_obj)
            self.viewport.update()
            self.transformMenu.close()

    def click_translate(self):
        obj_name = self.transformMenu.objListView.currentText()
        obj = self.world.getObj(obj_name)
        self._translate()

    def _translate(self):
        dx = float(self.transformMenu.desloc_x.text())
        dy = float(self.transformMenu.desloc_y.text())
        trans_mat = numpy.array([[1, 0, 0], [0, 1, 0], [dx, dy, 1]])

        self.transformMenu.trans_matrix = numpy.matmul(self.transformMenu.trans_matrix, trans_mat)
        self.transformMenu.logger.appendPlainText(f"-> TRANSLAÇÃO  Eixo X: {dx}    Eixo Y: {dy}\n")
        #     if isinstance(obj, Point):
        #     elif isinstance(obj, Line):
        #     # x1 = obj.getX1_Y1().index(0)
        #     # y1 = obj.getX1_Y1().index(1)
        #     # x2 = obj.getX2_Y2().index(0)
        #     # y2 = obj.getX2_Y2().index(1)
        #     # x_y1 = numpy.array([[x1, y1, 1]])
        #     # x_y2 = numpy.array([[x2, y2, 1]])
        #     # new_x1_y1 = numpy.matmul(x_y1, trans_mat)
        #     # new_x1_y1 = numpy.matmul(x_y2, trans_mat)
        #
        #     self.transformMenu.trans_matrix = numpy.matmul(self.transformMenu.trans_matrix, trans_mat)
        #     self.transformMenu.logger.appendPlainText(f"-> TRANSLAÇÃO  Eixo X: {dx}    Eixo Y: {dy}\n")
        #
        # elif isinstance(obj, Wireframe):
        #     result = list()
        #     for x_y in obj.getCoords():
        #         x = x_y.index(0)
        #         y = x_y.index(1)
        #         matrix = numpy.array([[x, y, 1]])
        #         result.append(numpy.matmul(matrix, trans_mat))
        # #     TODO atualizar obj

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
