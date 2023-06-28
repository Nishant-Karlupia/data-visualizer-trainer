import sys
import pandas as pd
from PyQt5.QtWidgets import QMainWindow,QWidget,QApplication,QPushButton,QVBoxLayout,QTableView,QFileDialog,QHeaderView,QLineEdit,QHBoxLayout,QGraphicsDropShadowEffect,QMessageBox
from PyQt5.QtGui import QStandardItem,QStandardItemModel,QColor
from PyQt5.QtCore import Qt
from CustomFunction import Open_Datafile,apply_stylesheet


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Show the data")
        self.setMinimumSize(500,500)

        widget=QWidget()
        self.open_btn=QPushButton("Open File")
        self.open_btn.clicked.connect(self.open_file)
        self.open_btn.setObjectName("open_btn")

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(8)
        shadow.setColor(QColor(0, 0, 0, 100))
        shadow.setOffset(0, 2)
        self.open_btn.setCursor(Qt.PointingHandCursor)
        self.open_btn.setGraphicsEffect(shadow)
        
        
        self.sep=QLineEdit()
        self.sep.setPlaceholderText("Enter the separator (; , ...etc)")
        self.sep.setObjectName("separator")

        

        self.model=QStandardItemModel()
        table=QTableView()
        table.setModel(self.model)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        hbox=QHBoxLayout()
        hbox.addWidget(self.open_btn)
        hbox.addWidget(self.sep)
        
        layout=QVBoxLayout()
        layout.addLayout(hbox)
        layout.addWidget(table)
        widget.setLayout(layout)


        self.setCentralWidget(widget)

        apply_stylesheet(self,'data_model.qss')


    def open_file(self):

        res=Open_Datafile(self,self.sep)

        if res[0]==None:
            return

        if res[0]==False:
            msg_box=QMessageBox.critical(self,"Error!!!","Make sure that file is .xlsx or .csv")
            return
        
        df=res[1]   
        columns=list(df.columns)
        # print(columns)
        self.model.setColumnCount(len(columns))
        self.model.setHorizontalHeaderLabels(columns)

        for ind,value in enumerate(df.values):
            # print(df.value)
            items=[QStandardItem(str(val)) for val in value]
            self.model.insertRow(ind,items)

    

if __name__=="__main__":
    app=QApplication(sys.argv)
    window=MainWindow()
    window.show()
    sys.exit(app.exec_())