import sys
from PyQt5.QtWidgets import QWidget,QMainWindow,QApplication

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()


if __name__=="__main__":
    app=QApplication(sys.argv)
    window=MainWindow()
    window.show()
    sys.exit(app.exec_())