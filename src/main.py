import sys
from PyQt5.QtWidgets import QApplication, QWidget
from window import MainWindow


def main():
    app = QApplication(sys.argv)
    mainWindow = MainWindow().loadWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
