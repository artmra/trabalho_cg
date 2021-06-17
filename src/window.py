from PyQt5.QtWidgets import QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.top_ = 100
        self.left_ = 100
        self.width_ = 800
        self.height_ = 600
        self.title_ = "Trabalho CG - Arthur Moreira R Alves & Bryan Martins Lima"

    def loadWindow(self):
        self.setGeometry(self.left_, self.top_, self.width_, self.height_)
        self.setWindowTitle(self.title_)
        self.show()
