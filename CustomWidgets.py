import sys
from PyQt5.QtWidgets import QGraphicsDropShadowEffect,QGraphicsView,QPushButton,QListWidget,QListWidgetItem
from PyQt5.QtChart import QChartView
from PyQt5.QtGui import QColor,QDrag
from PyQt5.QtCore import Qt,QMimeData


class ChartView(QChartView):
    def __init__(self,chart):
        super().__init__(chart)
        self.chart=chart
        self.start_pos=None


    def wheelEvent(self, event):
        zoom,scale=1,1.10

        if event.angleDelta().y()>=120 and zoom<3:
            zoom*=1.25
            self.chart.zoom(scale)

        elif event.angleDelta().y()<=-120 and zoom>0.5:
            zoom*=0.8
            self.chart.zoom(1/scale)

        
    def mousePressEvent(self, event):
        if event.button()==Qt.LeftButton:
            self.setDragMode(QGraphicsView.ScrollHandDrag)
            self.start_pos=event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons()==Qt.LeftButton:
            delta=self.start_pos-event.pos()
            self.chart.scroll(delta.x(),-delta.y())
            self.start_pos=event.pos()

    def mouseReleaseEvent(self, event):
        self.setDragMode(QGraphicsView.NoDrag)


class FirstButton(QPushButton):
    def __init__(self,text,objectName=None,slot=None):
        super().__init__()
        self.setText(text)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(8)
        shadow.setColor(QColor(0, 0, 0, 100))
        shadow.setOffset(0, 2)
        self.setCursor(Qt.PointingHandCursor)
        self.setGraphicsEffect(shadow)

        if slot!=None:
            self.clicked.connect(slot)
        if objectName!=None:
            self.setObjectName(objectName)


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

