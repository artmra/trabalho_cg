import numpy
from PyQt5.QtGui import QIcon, QPixmap, QPalette, QColor
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox, QGroupBox, \
    QTabWidget, QPlainTextEdit, QFormLayout, QStackedLayout, QVBoxLayout
from objs import Point, Line, Wireframe
from viewport import Viewport


# classe base com elementos comuns a todas as classes de criacao de obj
class CreateMenu(QWidget):
    def __init__(self, name, viewport: Viewport, objListView: QComboBox):
        super().__init__()
        self.setWindowTitle(name)
        self.viewport = viewport
        self.objListView = objListView
        self.createButton = QPushButton('Criar')
        # self.createButton.setStyleSheet('border: none')
        self.cancelButton = QPushButton('Cancelar')
        # self.cancelButton.setStyleSheet('border: none')
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
            if obj in self.viewport.world.objs:
                msg = QMessageBox()
                msg.setWindowTitle('Erro no processo de criação')
                msg.setText('Não é possível criar objetos com o mesmo nome ou informações parecidas.')
                x = msg.exec_()
            else:
                self.viewport.addObj(obj)
                self.objListView.addItem(obj.name)
                self.viewport.update()
                self.close()
        except Exception as e:
            msg = QMessageBox()
            msg.setWindowTitle('Erro no processo de criação')
            msg.setWindowIcon(QIcon('warning.svg'))
            msg.setText(str(e))
            x = msg.exec_()


# janela de criacao de linha
class CreateLineMenu(CreateMenu):
    def __init__(self, viewport: Viewport, objListView: QComboBox):
        super().__init__('Criação de Linha', viewport, objListView)
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
            if obj in self.viewport.world.objs:
                msg = QMessageBox()
                msg.setWindowTitle('Erro no processo de criação')
                msg.setText('Não é possível criar objetos com o mesmo nome ou informações parecidas.')
                x = msg.exec_()
            else:
                self.viewport.addObj(obj)
                self.objListView.addItem(obj.name)
                self.viewport.update()
                self.close()
        except Exception as e:
            msg = QMessageBox()
            msg.setWindowTitle('Erro no processo de criação')
            msg.setText(str(e))
            x = msg.exec_()

class CreateTransformMenu(CreateMenu):
    def __init__(self, viewport: Viewport, objListView: QComboBox):
        super().__init__('Transformação de objeto', viewport, objListView)
        layout = QGridLayout()
        self.setLayout(layout)
        self.trans_matrix = numpy.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])


        transform_group = QGroupBox('Transformações')
        transform_group.setFixedSize(500, 300)
        layout.addWidget(transform_group)

        self.transformButton = QPushButton('Fazer Transformações')
        layout.addWidget(self.transformButton, 1, 0)
        layout.addWidget(self.cancelButton, 1, 1)
        self.cancelButton.clicked.connect(self.close)

        self.logger = QPlainTextEdit()
        obj_name = objListView.currentText()
        self.logger.setStyleSheet("background-color: rgb(230, 230, 230)")
        self.logger.appendPlainText(f'-> Lista de Transformações do objeto {obj_name}:')
        self.logger.setReadOnly(True)
        self.logger.setFixedSize(250, 300)
        layout.addWidget(self.logger, 0, 1)

        tab_layout = QGridLayout()
        transform_group.setLayout(tab_layout)

        tabs = QTabWidget()
        tabs.resize(300, 200)

        # Scale Translate and Rotate menu
        tabScale = self.create_scale_menu()
        tabTranslate = self.create_translate_menu()
        tabRotate = self.create_rotate_menu()

        tabs.addTab(tabScale, "Escalonar")
        tabs.addTab(tabTranslate, "Transladar")
        tabs.addTab(tabRotate, "Rotacionar")
        tab_layout.addWidget(tabs)

    def create_scale_menu(self) -> QWidget:
        tabScale = QWidget()
        tabScale.layout = QGridLayout()
        tabScale.setLayout(tabScale.layout)
        tabScale.layout.addWidget(QLabel('Escala no eixo X:'), 0, 0)
        self.scale_x = QLineEdit()
        tabScale.layout.addWidget(self.scale_x, 0, 1)

        tabScale.layout.addWidget(QLabel('Escala no eixo Y:'), 1, 0)
        self.scale_y = QLineEdit()
        tabScale.layout.addWidget(self.scale_y, 1, 1)

        self.scale_save_button = QPushButton('Salvar')
        # TODO conectar função para salvar matriz de escalonamento
        # self.saveButton.clicked.connect(self.clicked_save_button)
        tabScale.layout.addWidget(self.scale_save_button, 2, 0)

        return tabScale


    def create_translate_menu(self) -> QWidget:
        tabTranslate = QWidget()
        tabTranslate.layout = QGridLayout()
        tabTranslate.setLayout(tabTranslate.layout)
        tabTranslate.layout.addWidget(QLabel('Deslocamento no eixo X:'), 0, 0)
        self.desloc_x = QLineEdit()
        tabTranslate.layout.addWidget(self.desloc_x, 0, 1)

        tabTranslate.layout.addWidget(QLabel('Deslocamento no eixo Y:'), 1, 0)
        self.desloc_y = QLineEdit()
        tabTranslate.layout.addWidget(self.desloc_y, 1, 1)

        self.translate_save_button = QPushButton('Salvar')
        tabTranslate.layout.addWidget(self.translate_save_button, 2, 0)

        return tabTranslate

    def clicked_translate_button(self):
        print(self.desloc_x.text())


    def create_rotate_menu(self) -> QWidget:
        tabTranslate = QWidget()
        tabTranslate.layout = QVBoxLayout()
        tabTranslate.setLayout(tabTranslate.layout)

        self.pageCombo = QComboBox()
        self.pageCombo.addItems(["Em torno do centro do mundo",
                                 "Em torno do centro do objeto",
                                 "Em torno de um ponto"])
        self.pageCombo.activated.connect(self.switchPage)

        self.stackedLayout = QStackedLayout()


        # Pagina centro do mundo
        page_1 = QWidget()
        page_1.layout = QFormLayout()
        page_1.setLayout(page_1.layout)
        self.angle1 = QLineEdit()
        page_1.layout.addRow("Angulo em graus", self.angle1)
        self.save_world_center_button = QPushButton('Salvar')
        page_1.layout.addRow(self.save_world_center_button)
        self.stackedLayout.addWidget(page_1)

        # Pagina centro do objeto
        page_2 = QWidget()
        page_2.layout = QFormLayout()
        page_2.setLayout(page_2.layout)
        self.angle2 = QLineEdit()
        page_2.layout.addRow("Angulo em graus", self.angle2)
        self.save_obj_center_button = QPushButton('Salvar')
        page_2.layout.addRow(self.save_obj_center_button)
        self.stackedLayout.addWidget(page_2)

        # Pagina em torno de um ponto
        page_3 = QWidget()
        page_3.layout = QFormLayout()
        page_3.setLayout(page_3.layout)
        self.angle3 = QLineEdit()
        self.x3 = QLineEdit()
        self.y3 = QLineEdit()
        page_3.layout.addRow("Angulo em graus", self.angle3)
        page_3.layout.addRow("Ponto eixo x", self.x3)
        page_3.layout.addRow("Ponto eixo y", self.y3)
        self.save_point_button = QPushButton('Salvar')
        page_3.layout.addRow(self.save_point_button)
        self.stackedLayout.addWidget(page_3)

        tabTranslate.layout.addWidget(self.pageCombo)
        tabTranslate.layout.addLayout(self.stackedLayout)

        return tabTranslate

    def switchPage(self):
        self.stackedLayout.setCurrentIndex(self.pageCombo.currentIndex())

# janela de criacao de poligonos
class CreateWireframeMenu(CreateMenu):
    def __init__(self, viewport: Viewport, objListView: QComboBox, inputCoords=None):
        super().__init__('Criação de Linha', viewport, objListView)
        self.createButton.clicked.connect(self.clickCreate)
        self.addCoordButton = QPushButton()
        self.addCoordButton.setStyleSheet('border: none')
        self.addCoordButton.setIcon(QIcon(QPixmap('addCoord.svg')))
        self.inputCoords = [(QLineEdit(), QLineEdit()), (QLineEdit(), QLineEdit()), (QLineEdit(), QLineEdit())] if inputCoords is None else inputCoords
        self.loadLayout()
        self.addCoordButton.clicked.connect(self.updateLayout)

    def clickCreate(self):
        try:
            coords = [(xyin[0].text(), xyin[1].text()) for xyin in self.inputCoords]
            obj = Wireframe(self.name.text(), coords)
            if obj in self.viewport.world.objs:
                msg = QMessageBox()
                msg.setWindowTitle('Erro no processo de criação')
                msg.setText('Não é possível criar objetos com o mesmo nome ou informações parecidas.')
                x = msg.exec_()
            else:
                self.viewport.addObj(obj)
                self.objListView.addItem(obj.name)
                self.viewport.update()
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

