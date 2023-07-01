import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow,QApplication,QWidget,QHBoxLayout,QPushButton
from graph_between_variables import MainWindow as Graph
from dashboard import MainWindow as DashBoard
from CustomWidgets import CustomMessageBox,FirstButton

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.box=None
        self.setMinimumSize(300,200)
        widget=QWidget()
        layout=QHBoxLayout()
        btn=FirstButton("Dialog","btn",self.open_dialog)
        layout.addWidget(btn)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def open_dialog(self):
        self.box=CustomMessageBox("Error!!!","File Not opened")
        self.box.show()
        # pass

    def closeEvent(self, event):
        if self.box!=None:
            self.box.close()

if __name__=="__main__":
    app=QApplication(sys.argv)
    window=MainWindow()
    window.show()
    sys.exit(app.exec_())