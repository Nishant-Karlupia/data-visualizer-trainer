import sys
from PyQt5.QtWidgets import QApplication,QWidget,QLabel,QCheckBox
from PyQt5.QtCore import Qt

class CheckBoxWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.InitializeUI()

    def InitializeUI(self):
        self.setGeometry(100,100,300,300)
        self.setWindowTitle("PyQt CheckBox")
        self.displayCheckBoxes()
        self.show()

    def displayCheckBoxes(self):
        header=QLabel("Which shifts can you work?",self)
        header.move(10,10)
        header.resize(230,60)

        morning=QCheckBox("Morning [8 AM-2 PM]",self)
        morning.move(20,80)
        morning.toggle()
        morning.stateChanged.connect(self.displayAnswer)

        afternoon=QCheckBox("Afternoon [1 PM-8 PM]",self)
        afternoon.move(20,100)
        # afternoon.toggle()
        afternoon.stateChanged.connect(self.displayAnswer)

        evening=QCheckBox("Evening [7 PM-3 AM]",self)
        evening.move(20,120)
        # evening.toggle()
        evening.stateChanged.connect(self.displayAnswer)

    def displayAnswer(self):
        sender=self.sender()
        if sender.isChecked():
            print("{} selected".format(sender.text()))
        else:
            print("{} deselected".format(sender.text()))
    
if __name__=='__main__':
    app=QApplication(sys.argv)
    window=CheckBoxWindow()
    sys.exit(app.exec())