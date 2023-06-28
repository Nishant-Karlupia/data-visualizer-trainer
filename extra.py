import sys
import typing
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication,QMainWindow,QWidget,QListWidget,QListWidgetItem,QHBoxLayout
from PyQt5.QtGui import QDrag,QPalette,QColor,QCursor
from PyQt5.QtCore import QMimeData,Qt 


class CustomListWidget(QListWidget):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setDragEnabled(True)

    # def mousePressEvent(self,event):
    #     if event.button()==Qt.LeftButton:
    #         items=self.selectedItems()
    #         if(len(items)<=0):
    #             return
    #         drag=QDrag(self)
    #         mime=QMimeData()
    #         mime.setText(items[0].text())
    #         drag.setMimeData(mime)
    #         drag.exec(Qt.MoveAction)

    #     super().mousePressEvent(event)

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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.list1=CustomListWidget()
        self.list2=CustomListWidget()

        widget=QWidget()
        layout=QHBoxLayout()
        layout.addWidget(self.list1)
        layout.addWidget(self.list2)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.add_items()

    def add_items(self):
        for i in range(1,6):
            item=QListWidgetItem("List_1: "+str(i))
            self.list1.addItem(item)
        for i in range(1,6):
            item=QListWidgetItem("List_2: "+str(i))
            self.list2.addItem(item)

    

if __name__=="__main__":
    app=QApplication(sys.argv)
    window=MainWindow()
    window.show()
    sys.exit(app.exec_())