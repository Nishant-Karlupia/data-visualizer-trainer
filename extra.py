from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5.QtCore import QPropertyAnimation, QRect, QEventLoop, QTimer

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Minimize/Maximize Example")

        minimize_button = QPushButton("Minimize", self)
        minimize_button.clicked.connect(self.minimize_window)

        maximize_button = QPushButton("Maximize", self)
        maximize_button.clicked.connect(self.maximize_window)

        self.setCentralWidget(minimize_button)
        self.statusBar().addWidget(maximize_button)

    def minimize_window(self):
        # Create a property animation for the window geometry
        animation = QPropertyAnimation(self, b"geometry")
        animation.setDuration(500)  # Animation duration in milliseconds

        # Define the start and end geometries for the animation
        start_geometry = self.geometry()
        end_geometry = QRect(start_geometry.x(), start_geometry.y(),
                             start_geometry.width(), 0)

        # Set the start and end values for the animation
        animation.setStartValue(start_geometry)
        animation.setEndValue(end_geometry)

        # Start the animation
        animation.start()

        # Process events and wait for the animation to finish
        loop = QEventLoop()
        animation.finished.connect(loop.quit)
        loop.exec_()

        # After the animation finishes, minimize the window
        self.showMinimized()

    def maximize_window(self):
        # Create a property animation for the window geometry
        animation = QPropertyAnimation(self, b"geometry")
        animation.setDuration(500)  # Animation duration in milliseconds

        # Define the start and end geometries for the animation
        start_geometry = self.geometry()
        end_geometry = self.normalGeometry()

        # Set the start and end values for the animation
        animation.setStartValue(start_geometry)
        animation.setEndValue(end_geometry)

        # Start the animation
        animation.start()

        # Process events and wait for the animation to finish
        loop = QEventLoop()
        animation.finished.connect(loop.quit)
        loop.exec_()

        # After the animation finishes, maximize the window
        self.showMaximized()


if __name__ == '__main__':
    app = QApplication([])
    main_window = MyMainWindow()
    main_window.show()
    app.exec_()
