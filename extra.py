from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Open Link Example")

        self.open_link_btn = QPushButton("Open Link", self)
        self.open_link_btn.clicked.connect(self.open_link)

    def open_link(self):
        url = QUrl("https://www.google.com")  # Replace with your desired link
        QDesktopServices.openUrl(url)

if __name__ == '__main__':
    app = QApplication([])
    main_window = MyMainWindow()
    main_window.show()
    app.exec_()
