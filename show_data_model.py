import sys
import pandas as pd
from PyQt5.QtWidgets import QMainWindow,QWidget,QApplication,QPushButton,QVBoxLayout,QTableView,QFileDialog,QHeaderView,QLineEdit,QHBoxLayout,QGraphicsDropShadowEffect
from PyQt5.QtGui import QStandardItem,QStandardItemModel,QColor
from PyQt5.QtCore import Qt


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

        self.apply_stylesheet()


    def apply_stylesheet(self):
        stylesheet=None
        with open('data_model.qss', 'r') as f:
            stylesheet = f.read()
        self.setStyleSheet(stylesheet)
        f.close()


    def open_file(self):
        filename,_=QFileDialog.getOpenFileName(self,"Open File","","All Files(*)")
        if filename:
            # print("Open")
            df,get=None,False
            sep=self.sep.text()
            # print(sep)
            if filename.endswith(".csv"):
                if len(sep)>0:
                    df=pd.read_csv(filename,sep=sep)
                else:
                    df=pd.read_csv(filename)
                get=True
            if filename.endswith(".xlsx"):
                if len(sep)>0:
                    df=pd.read_excel(filename,sep=sep)
                else:
                    df=pd.read_excel(filename)
                get=True
            
            if not get:
                print("Not able to open data file")
                return
            
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