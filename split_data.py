import sys
from PyQt5 import QtGui
import pandas as pd
from PyQt5.QtWidgets import QMainWindow,QWidget,QApplication,QPushButton,QVBoxLayout,QTableView,QFileDialog,QHeaderView,QLineEdit,QHBoxLayout,QGraphicsDropShadowEffect,QMessageBox,QListWidget,QListWidgetItem,QLabel,QGridLayout
from PyQt5.QtGui import QColor,QDrag
from PyQt5.QtCore import Qt,QMimeData

class CustomListWidget(QListWidget):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setDragEnabled(True)


    def startDrag(self, supportedActions):
        items=self.selectedItems()
        if len(items)<=0:
            return

        data=QMimeData()
        data.setText(items[0].text())
        drag=QDrag(self)
        drag.setMimeData(data)
        drag.exec(Qt.MoveAction)

    
    def dragEnterEvent(self,event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        if event.mimeData().hasText():
            text=event.mimeData().text()
            item=QListWidgetItem(str(text))
            self.addItem(item)
            event.acceptProposedAction()
            event.setDropAction(Qt.MoveAction)

            source=event.source()
            source.takeItem(source.row(source.currentItem()))



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

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(8)
        shadow.setColor(QColor(0, 0, 0, 100))
        shadow.setOffset(0, 2)

        self.confirm_btn=QPushButton("OK")
        self.confirm_btn.clicked.connect(lambda: self.work_done(x_col,y_col))
        self.confirm_btn.setObjectName("confirm_btn")
        self.confirm_btn.setCursor(Qt.PointingHandCursor)
        self.confirm_btn.setGraphicsEffect(shadow)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(8)
        shadow.setColor(QColor(0, 0, 0, 100))
        shadow.setOffset(0, 2)
        
        self.close_btn=QPushButton("Close")
        self.close_btn.clicked.connect(self.close)
        self.close_btn.setObjectName("close_btn")
        self.close_btn.setCursor(Qt.PointingHandCursor)
        self.close_btn.setGraphicsEffect(shadow)

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

        self.apply_stylesheet()


    def apply_stylesheet(self):
        stylesheet=None
        with open('split_data.qss', 'r') as f:
            stylesheet = f.read()
        f.close()

        try:
            self.setStyleSheet(stylesheet)
        except:
            pass


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

        hbox=QHBoxLayout()
        hbox.addWidget(self.open_btn)
        hbox.addWidget(self.sep)
        
        layout=QVBoxLayout()
        layout.addLayout(hbox)
        widget.setLayout(layout)


        self.setCentralWidget(widget)

        self.apply_stylesheet()


    def apply_stylesheet(self):
        stylesheet=None
        with open('split_data.qss', 'r') as f:
            stylesheet = f.read()
        f.close()

        try:
            self.setStyleSheet(stylesheet)
        except:
            pass


    def open_file(self):
        if(len(self.x_col)!=0 and len(self.y_col)!=0):
            print(self.x_col)
            print(self.y_col)
        filename,_=QFileDialog.getOpenFileName(self,"Open File","","All Files(*)")
        if filename:
            # print("Open")
            get=False
            sep=self.sep.text()
            # print(sep)
            if filename.endswith(".csv"):
                if len(sep)>0:
                    self.df=pd.read_csv(filename,sep=sep)
                else:
                    self.df=pd.read_csv(filename)
                get=True
            if filename.endswith(".xlsx"):
                if len(sep)>0:
                    self.df=pd.read_excel(filename,sep=sep)
                else:
                    self.df=pd.read_excel(filename)
                get=True
            
            if not get:
                # print("Not able to open data file")
                QMessageBox.critical(self,"Error!!!","Make sure that file is .xlsx or .csv")
                return
            
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