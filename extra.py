import sys
import pandas as pd
from PyQt5.QtWidgets import QWidget,QMainWindow,QApplication,QVBoxLayout
from pipelines import SplitWindow

columns=['A','B',"C","D","E"]
xcol,ycol=[],[]

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        layout=QVBoxLayout()
        processing_window=SplitWindow(columns,xcol,ycol)
        layout.addWidget(processing_window)
        widget=QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)




if __name__=="__main__":
    app=QApplication(sys.argv)
    window=MainWindow()
    window.show()
    sys.exit(app.exec_())