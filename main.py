import sys
from PyQt5.QtWidgets import QMainWindow,QApplication,QWidget,QHBoxLayout,QPushButton
from graph_between_variables import MainWindow as Graph
from dashboard import MainWindow as DashBoard

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        widget=QWidget()
        layout=QHBoxLayout()
        window=DashBoard()
        layout.addWidget(window)

        btn=QPushButton("Button")
        layout.addWidget(btn)


        widget.setLayout(layout)
        self.setCentralWidget(widget)

if __name__=="__main__":
    app=QApplication(sys.argv)
    window=MainWindow()
    window.show()
    sys.exit(app.exec_())