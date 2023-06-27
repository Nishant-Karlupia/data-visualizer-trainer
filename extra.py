from PyQt5.QtCore import Qt, QPropertyAnimation, QRect
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QPushButton

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.sidebar_width = 200
        self.sidebar_minimum_width = 50
        self.is_sidebar_visible = True

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.sidebar = QWidget()
        self.sidebar.setStyleSheet("background-color: lightgray;")
        self.sidebar.setMinimumWidth(self.sidebar_minimum_width)
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setAlignment(Qt.AlignTop)
        layout.addWidget(self.sidebar)

        self.body = QWidget()
        self.body.setStyleSheet("background-color: white;")
        layout.addWidget(self.body)

        self.toggle_button = QPushButton("Toggle Sidebar")
        self.toggle_button.clicked.connect(self.toggle_sidebar)
        self.sidebar_layout.addWidget(self.toggle_button)

    def toggle_sidebar(self):
        if self.is_sidebar_visible:
            self.animate_sidebar_width(self.sidebar_width, 0)
        else:
            self.animate_sidebar_width(0, self.sidebar_width)
        self.is_sidebar_visible = not self.is_sidebar_visible

    def animate_sidebar_width(self, start_width, end_width):
        animation = QPropertyAnimation(self.sidebar, b"geometry")
        animation.setDuration(300)
        animation.setStartValue(QRect(0, 0, start_width, self.sidebar.height()))
        animation.setEndValue(QRect(0, 0, end_width, self.sidebar.height()))
        animation.start()

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
