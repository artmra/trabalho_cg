import numpy
from PyQt5.QtGui import QIcon
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
        self.coords = QLineEdit()
        self.rgb = QLineEdit()
        self.name = QLineEdit()
        self.createButton = QPushButton('Criar')
        self.cancelButton = QPushButton('Cancelar')
        self.cancelButton.clicked.connect(self.close)

    def verify_duplicate_obj(self, obj):
        if obj in self.viewport.world.objs:
            msg = QMessageBox()
            msg.setWindowTitle('Erro no processo de criação')
            msg.setText('Não é possível criar objetos com o mesmo nome ou informações parecidas.')
            msg.exec_()
        else:
            self.viewport.addObj(obj)
            self.objListView.addItem(obj.name)
            self.viewport.update()
            self.close()

    def create_generic_menu(self):
        layout = QGridLayout()
        layout.addWidget(QLabel('Nome:'), 0, 0)
        layout.addWidget(self.name, 0, 1)
        layout.addWidget(QLabel('Coordenada:'), 1, 0)
        layout.addWidget(self.coords, 1, 1)
        layout.addWidget(QLabel('Valores RGB:'), 2, 0)
        layout.addWidget(self.rgb, 2, 1)
        layout.addWidget(self.createButton, 3, 0)
        layout.addWidget(self.cancelButton, 3, 1)
        self.setLayout(layout)


# janela de criacao de pontos
class CreatePointMenu(CreateMenu):
    def __init__(self, viewport: Viewport, objListView: QComboBox):
        super().__init__('Criação de Ponto', viewport, objListView)
        self.createButton.clicked.connect(self.clickCreate)
        self.create_generic_menu()
        self.setFixedSize(270, 200)

    def clickCreate(self):
        try:
            coords = tuple(eval(self.coords.text()))
            try:
                rgb = tuple(eval(self.rgb.text()))
                obj = Point(self.name.text(), coords, rgb)
            except:
                obj = Point(self.name.text(), coords)
            self.verify_duplicate_obj(obj)
        except Exception as e:
            msg = QMessageBox()
            msg.setWindowTitle('Erro no processo de criação')
            msg.setWindowIcon(QIcon('warning.svg'))
            msg.setText(str(e))
            msg.exec_()


# janela de criacao de linha
class CreateLineMenu(CreateMenu):
    def __init__(self, viewport: Viewport, objListView: QComboBox):
        super().__init__('Criação de Linha', viewport, objListView)
        self.createButton.clicked.connect(self.clickCreate)
        self.create_generic_menu()
        self.setFixedSize(280, 200)

    def clickCreate(self):
        try:
            coords = list(tuple(eval(self.coords.text())))
            try:
                rgb = tuple(eval(self.rgb.text()))
                obj = Line(self.name.text(), coords, rgb)
            except:
                obj = Line(self.name.text(), coords)
            self.verify_duplicate_obj(obj)
        except Exception as e:
            msg = QMessageBox()
            msg.setWindowTitle('Erro no processo de criação')
            msg.setText(str(e))
            msg.exec_()


# janela de criacao de poligonos
class CreateWireframeMenu(CreateMenu):
    def __init__(self, viewport: Viewport, objListView: QComboBox, inputCoords=None):
        super().__init__('Criação de Linha', viewport, objListView)
        self.createButton.clicked.connect(self.clickCreate)
        self.create_generic_menu()
        self.setFixedSize(400, 200)

    def clickCreate(self):
        try:
            coords = tuple(eval(self.coords.text()))
            try:
                rgb = tuple(eval(self.rgb.text()))
                obj = Wireframe(self.name.text(), coords, rgb)
            except:
                obj = Wireframe(self.name.text(), coords)
            self.verify_duplicate_obj(obj)
        except Exception as e:
            msg = QMessageBox()
            msg.setWindowTitle('Erro no processo de criação')
            msg.setText(str(e))
            msg.exec_()


# janela de realização de transformacoes
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

        # liga funcoes de transformacao aos seus botoes
        self.translate_save_button.clicked.connect(lambda: self.viewport.world._translate(transformMenu=self))
        self.scale_save_button.clicked.connect(lambda: self.viewport.world._scale(transformMenu=self, current_obj_name=self.objListView.currentText()))
        self.save_point_button.clicked.connect(lambda: self.viewport.world.click_rotate_point(transformMenu=self, current_obj_name=self.objListView.currentText()))
        self.save_world_center_button.clicked.connect(lambda: self.viewport.world.click_rotate_world(transformMenu=self, current_obj_name=self.objListView.currentText()))
        self.save_obj_center_button.clicked.connect(lambda: self.viewport.world.click_rotate_obj(transformMenu=self, current_obj_name=self.objListView.currentText()))
        self.transformButton.clicked.connect(lambda: self.viewport.world.click_transform(transformMenu=self, current_obj_name=self.objListView.currentText(), viewport=self.viewport))

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