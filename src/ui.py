from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QPushButton, QGridLayout, QVBoxLayout, QComboBox, QGroupBox, QMainWindow, QLabel, \
    QMessageBox, QAction, QFileDialog, QRadioButton

from createMenus import CreatePointMenu, CreateLineMenu, CreateWireframeMenu, CreateTransformMenu
from objs import DescritorOBJ
from world import World
from viewport import Viewport


class Ui(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(1110, 810)
        self.setWindowTitle('T1 - Arthur M R Alves & Bryan M Lima')
        self.setWindowIcon(QIcon('uiIcon.png'))
        self.objListView = QComboBox()
        self.menubar = self.menuBar()
        self.filemenu = self.menubar.addMenu('File')
        self.createActionsMenuBar()
        # import_action = QAction('Import File', self)
        # export_action = QAction('Export objects to file', self)
        # filemenu.addAction(import_action)
        # filemenu.addAction(export_action)
        # world
        self.world = World()

        # descritor = DescritorOBJ()
        # descritor.importObj('objs/teste.obj')

        # viewport
        self.viewport = Viewport(self.world)
        self.viewport.setParent(self)
        self.viewport.move(305, 5)
        # menu com as funcionalidades da aplicação
        self.funcMenu = self.createFuncMenu()
        self.funcMenu.setParent(self)
        self.funcMenu.move(5, 5)

    def createActionsMenuBar(self):
        # Import action
        importAction = QAction("Import", self)
        # TODO connect with fileopen action
        importAction.triggered.connect(self.importDialog)
        self.filemenu.addAction(importAction)
        # Export action
        exportAction = QAction("Export", self)
        exportAction.triggered.connect(self.exportDialog)
        self.filemenu.addAction(exportAction)

    def importDialog(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Import File", "", "Obj Files (*.obj)")
        if filename:
            descritor = DescritorOBJ()
            error = descritor.importObj(filename)
            if error:
                msg = QMessageBox()
                msg.setWindowTitle('Erro ao importar o arquivo!')
                msg.setText(f'O seguinte erro ocorreu durante a leitura do arquivo:\n{error}')
                msg.exec_()
            if descritor.list_objs:
                for obj in descritor.list_objs:
                    self.viewport.addObj(obj)
                    self.objListView.addItem(obj.name)

    def exportDialog(self):
        fileName, _ = QFileDialog.getSaveFileName(self, "Export File", "objects.obj", "Obj Files (*.obj)")
        if fileName:
            descritor = DescritorOBJ()
            file_content = descritor.exportObj(self.world)
            file = open(fileName, 'w')
            file.write(file_content)
            file.close()

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
        movMenu.setFixedSize(250, 350)
        layout = QGridLayout()
        layout.addWidget(QLabel('Movimentação:'), 0, 0, 1, 3)
        upButton = QPushButton()
        upButton.setIcon(QIcon(QPixmap('up.svg')))
        upButton.setFlat(True)
        upButton.clicked.connect(self.clickMoveUp)
        layout.addWidget(upButton, 1, 1, 1, 2)
        leftButton = QPushButton()
        leftButton.setIcon(QIcon(QPixmap('left.svg')))
        leftButton.setFlat(True)
        leftButton.clicked.connect(self.clickMoveLeft)
        layout.addWidget(leftButton, 2, 0, 1, 2)
        rightButton = QPushButton()
        rightButton.setIcon(QIcon(QPixmap('right.svg')))
        rightButton.setFlat(True)
        rightButton.clicked.connect(self.clickMoveRight)
        layout.addWidget(rightButton, 2, 2, 1, 2)
        downButton = QPushButton()
        downButton.setIcon(QIcon(QPixmap('down.svg')))
        downButton.setFlat(True)
        downButton.clicked.connect(self.clickMoveDown)
        layout.addWidget(downButton, 3, 1, 1, 2)
        layout.addWidget(QLabel('Zoom:'), 4, 0, 1, 3)
        zoomInButton = QPushButton()
        zoomInButton.setIcon(QIcon(QPixmap('zoomin.svg')))
        zoomInButton.setFlat(True)
        zoomInButton.clicked.connect(self.clickZoomIn)
        layout.addWidget(zoomInButton, 5, 0, 1, 2)
        zoomOutButton = QPushButton()
        zoomOutButton.setIcon(QIcon(QPixmap('zoomout.svg')))
        zoomOutButton.setFlat(True)
        zoomOutButton.clicked.connect(self.clickZoomOut)
        layout.addWidget(zoomOutButton, 5, 2, 1, 2)
        layout.addWidget(QLabel('Rotação: '), 6, 0, 1, 3)
        rotateRightButton = QPushButton()
        rotateRightButton.setIcon(QIcon(QPixmap('rotate-right.svg')))
        rotateRightButton.setFlat(True)
        rotateRightButton.clicked.connect(self.clickRotateRight)
        layout.addWidget(rotateRightButton, 7, 2, 1, 2)
        rotateLefttButton = QPushButton()
        rotateLefttButton.setIcon(QIcon(QPixmap('rotate-left.svg')))
        rotateLefttButton.setFlat(True)
        rotateLefttButton.clicked.connect(self.clickRotateLeft)
        layout.addWidget(rotateLefttButton, 7, 0, 1, 2)
        layout.addWidget(QLabel('Clipping: '), 8, 0, 1, 3)
        layout.addWidget(QLabel('CohenSutherland'), 9, 0, 1, 3)
        clipping_1 = QRadioButton()
        clipping_1.clicked.connect(lambda: self.setWindowClipping(opt=1))
        layout.addWidget(clipping_1, 9, 3)
        layout.addWidget(QLabel('LiangBarsky'), 10, 0, 1, 3)
        clipping_2 = QRadioButton()
        clipping_2.clicked.connect(lambda: self.setWindowCliping(opt=2))
        layout.addWidget(clipping_2, 10, 3)
        clipping_3 = QRadioButton()
        layout.addWidget(QLabel('Nenhum'), 11, 0, 1, 3)
        clipping_3.clicked.connect(lambda: self.setWindowClipping(opt=0))
        clipping_3.setChecked(True)
        layout.addWidget(clipping_3, 11, 3)

        movMenu.setLayout(layout)
        return movMenu

    # determina o alg de clipping q deve ser usado
    def setWindowClipping(self, opt=0):
        if self.viewport.clippingAlg != opt:
            self.viewport.clippingAlg = opt
            self.viewport.update()

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
            self.transformMenu.show()

    def clickDelOjb(self):
        selectedItemName = self.objListView.currentText()
        self.viewport.deleteObj(selectedItemName)
        index = self.objListView.currentIndex()
        self.objListView.removeItem(index)

    def clickZoomIn(self):
        # todo: usar o meio do
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

    def clickRotateRight(self):
        self.viewport.rotateRight()

    def clickRotateLeft(self):
        self.viewport.rotateLeft()
