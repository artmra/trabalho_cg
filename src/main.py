import sys
from PyQt5.QtWidgets import QApplication, QWidget
from ui import Ui


def main():
    app = QApplication(sys.argv)
    mainWindow = Ui()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
