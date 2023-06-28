import sys
from PyQt5 import QtGui
import pandas as pd
from PyQt5.QtWidgets import QMainWindow,QWidget,QApplication,QPushButton,QVBoxLayout,QTableView,QFileDialog,QHeaderView,QLineEdit,QHBoxLayout,QGraphicsDropShadowEffect,QMessageBox,QListWidget,QListWidgetItem,QLabel,QGridLayout
from PyQt5.QtGui import QColor,QDrag
from PyQt5.QtCore import Qt,QMimeData
from CustomWidgets import CustomListWidget,FirstButton
from CustomFunction import apply_stylesheet,Open_Datafile

class SplitWindow(QMainWindow):
    def __init__(self,columns,x_col,y_col):
        super().__init__()

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setMinimumSize(750,380)

        self.list1=CustomListWidget()
        self.list1.addItems(columns)
        self.list1.currentItemChanged.connect(self.data_change_occur)
        train_label=QLabel("Train Variables")
        train_label.setObjectName("train")

        self.list2=CustomListWidget()
        self.list2.currentItemChanged.connect(self.data_change_occur)
        target_label=QLabel("Target Variables")
        target_label.setObjectName("target")

        

        self.confirm_btn=FirstButton("OK","confirm_btn",lambda: self.work_done(x_col,y_col))
        self.close_btn=FirstButton("Close","close_btn",self.close)
        

        widget=QWidget()
        layout=QVBoxLayout()

        item_layout=QGridLayout()

        item_layout.addWidget(train_label,0,0)
        item_layout.addWidget(self.list1,1,0)
        item_layout.addWidget(target_label,0,1)
        item_layout.addWidget(self.list2,1,1)

        btn_layout=QHBoxLayout()
        btn_layout.addWidget(self.confirm_btn)
        btn_layout.addWidget(self.close_btn)

        layout.addLayout(item_layout)
        layout.addLayout(btn_layout)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        apply_stylesheet(self,'split_data.qss')

    def work_done(self,x_col,y_col):
        x_col.clear()
        y_col.clear()
        for i in range(self.list1.count()):
            item=self.list1.item(i)
            x_col.append(item.text())
        for i in range(self.list2.count()):
            item=self.list2.item(i)
            y_col.append(item.text())

        self.confirm_btn.setEnabled(False)

    def data_change_occur(self):
        self.confirm_btn.setEnabled(True)

       
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.df,self.data_split,self.x_col,self.y_col=None,None,[],[]

        self.setWindowTitle("Show the data")
        self.setMinimumSize(500,500)

        widget=QWidget()
        self.open_btn=FirstButton("Open File","open_btn",self.open_file)
        
        
        self.sep=QLineEdit()
        self.sep.setPlaceholderText("Enter the separator (; , ...etc)")
        self.sep.setObjectName("separator")

        hbox=QHBoxLayout()
        hbox.addWidget(self.open_btn)
        hbox.addWidget(self.sep)
        
        layout=QVBoxLayout()
        layout.addLayout(hbox)
        widget.setLayout(layout)


        self.setCentralWidget(widget)

        apply_stylesheet(self,'split_data.qss')


    def open_file(self):
        if(len(self.x_col)!=0 and len(self.y_col)!=0):
            print(self.x_col)
            print(self.y_col)

        res=Open_Datafile(self,self.sep)

        if res[0]==None:
            return
        
        if res[0]==False:
            QMessageBox.critical(self,"Error!!!","Make sure that file is .xlsx or .csv")
            return
                
        self.df=res[1]
            
        self.x_col,self.y_col=[],[]
        
        self.data_split=SplitWindow(list(self.df.columns),self.x_col,self.y_col)
        self.data_split.show()

    def closeEvent(self,event):
        if self.data_split!=None:
            self.data_split.close()
            
    

if __name__=="__main__":
    app=QApplication(sys.argv)
    window=MainWindow()
    window.show()
    sys.exit(app.exec_())