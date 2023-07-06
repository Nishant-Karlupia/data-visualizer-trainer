import sys
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow,QWidget,QApplication,QVBoxLayout,QTableView,QHeaderView,QLineEdit,QHBoxLayout,QGraphicsDropShadowEffect,QMessageBox
from PyQt5.QtGui import QStandardItem,QStandardItemModel
from CustomFunction import Open_Datafile,apply_stylesheet
from CustomWidgets import FirstButton,CustomMessageBox
from globalParams.stateStore import store
from globalParams.dataStore import globalData


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.dataFrame=globalData.give_data()

        self.setWindowTitle("Show the data")
        self.setMinimumSize(500,500)
        self.msg_box=None

        widget=QWidget()
        self.open_btn=FirstButton("Open File","open_btn",self.open_file)
                
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

        apply_stylesheet(self,'styles/data_model.qss')
        self.show_model_function()


    def open_file(self):

        res=Open_Datafile(self,self.sep)

        if res[0]==None:# no file opened
            return

        if res[0]==False:# file not an excel or csv
            self.msg_box=CustomMessageBox("Error","Make sure that file is .xlsx or .csv")
            store.add(self.msg_box)
            self.msg_box.show()
            return
        
        self.dataFrame=res[1]   

        self.show_model_function()

    def show_model_function(self):

        if self.dataFrame is None:
            return

        globalData.assign_data(self.dataFrame)
        columns=list(self.dataFrame.columns)
        # print(columns)
        self.model.setColumnCount(len(columns))
        self.model.setHorizontalHeaderLabels(columns)

        for ind,value in enumerate(self.dataFrame.values):
            # print(df.value)
            items=[QStandardItem(str(val)) for val in value]
            self.model.insertRow(ind,items)

    def closeEvent(self, event):
        store.close()

    

if __name__=="__main__":
    app=QApplication(sys.argv)
    window=MainWindow()
    window.show()
    sys.exit(app.exec_())