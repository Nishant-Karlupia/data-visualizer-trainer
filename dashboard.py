import sys
from PyQt5 import QtGui, uic
from PyQt5.QtWidgets import QMainWindow,QApplication,QDesktopWidget,QPushButton,QSizePolicy
from PyQt5.QtCore import QPropertyAnimation,QEasingCurve
from PyQt5.QtGui import QPixmap,QIcon,QDesktopServices
from PyQt5.QtCore import Qt,QPoint,QRect,QUrl
from CustomFunction import apply_stylesheet
from globalData.stateStore import store
from graph_between_variables import MainWindow as Graph
from show_data_model import MainWindow as DataModel

GITHUB="https://github.com/Nishant-Karlupia"
LINKEDIN="https://www.linkedin.com/in/nishant-karlupia-7a474b279/"

class MainWindow(QMainWindow):

    global GITHUB,LINKEDIN

    def __init__(self):
        super().__init__()
        uic.loadUi("dashboard.ui",self)

        self.isScreenMaximized=False # change icon of maximization button based on current value
        self.window_width,self.window_height=self.width(),self.height()
        self.x_pos,self.y_pos=300,80

        self.desktop=QDesktopWidget()
        self.previous_pos=self.pos() # window movement when dragging the screen with mouseEvents


        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # minimize::toggle-window-screen-size::close-window
        self.operational.setMaximumHeight(50)
        # view-data::visualize-data::...
        self.sidebar.setMaximumWidth(200)

        self.operational.setLayout(self.operational_layout)
        self.body_frame.setLayout(self.layout_on_body_frame)

        self.toggle_sidebar.clicked.connect(self.toggle_window)# button to toggle the width of the sidebar
        self.visualize_data_btn.clicked.connect(self.visualize_data_function)
        self.minimize_btn.clicked.connect(self.show_minimized)
        self.maximize_btn.clicked.connect(self.show_maximized)
        self.close_btn.clicked.connect(self.close)
        self.view_data_btn.clicked.connect(self.show_data_model_function)
        self.github_link_btn.clicked.connect(lambda: self.open_url(GITHUB))
        self.linkedin_link_btn.clicked.connect(lambda: self.open_url(LINKEDIN))

        self.mainLayout.setContentsMargins(0,0,0,0)
        self.mainLayout.setSpacing(0)

        self.sidebar.setLayout(self.itemLayout)

        self.doStyling()
        apply_stylesheet(self,"styles/dashboard.qss")

        self.centralwidget.setLayout(self.mainLayout)# it is QWidget of .ui file and not QMainWindow

        self.setCentralWidget(self.centralwidget)# QMainWindow->QWidget


    def visualize_data_function(self):
        self.toggle_window()

        self.clear_layout(self.layout_on_body_frame)

        graph_widget=Graph()
        
        self.layout_on_body_frame.addWidget(graph_widget)

    def show_data_model_function(self):
        self.toggle_window()
        self.clear_layout(self.layout_on_body_frame)
        data_model_widget=DataModel()
        self.layout_on_body_frame.addWidget(data_model_widget)


    # clear layout of main-body-frame so components can be added or removed dynamically
    def clear_layout(self,layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)
            else:
                nested_layout = item.layout()
                if nested_layout:
                    self.clear_layout(nested_layout)
            del item
   
    # toggle the width of the sidebar
    def toggle_window(self):
        width,newWidth=self.sidebar.width(),0

        newWidth=[230,0][width>=150]

        # print(width,newWidth)

        self.animation=QPropertyAnimation(self.sidebar,b'maximumWidth')
        self.animation.setDuration(500)
        self.animation.setStartValue(width)
        self.animation.setEndValue(newWidth)
        self.animation.start()

    # minimize the window using opacity factor of the window
    def show_minimized(self):
        self.animate_minimization=QPropertyAnimation(self,b'windowOpacity')
        self.animate_minimization.setDuration(300)
        self.animate_minimization.setStartValue(1)
        self.animate_minimization.setEndValue(0)
        self.animate_minimization.setEasingCurve(QEasingCurve.OutQuart)
        self.animate_minimization.start()
        self.animate_minimization.finished.connect(self.after_minimization)

    def after_minimization(self):
        self.setWindowOpacity(1)
        self.setVisible(False)
        self.showMinimized()
        self.setVisible(True)

    # maximize the window screen or restore the window screen size to normal state
    def show_maximized(self):

        icon=None
        if self.isScreenMaximized:
            self.isScreenMaximized=False
            icon=QPixmap("icons/arrow-up-right.svg")

            self.animate_normal=QPropertyAnimation(self,b'geometry')
            self.animate_normal.setDuration(100)
            self.animate_normal.setStartValue(self.geometry())
            self.animate_normal.setEndValue(QRect(self.x_pos,self.y_pos,self.window_width,self.window_height))
            self.animate_normal.start()
        else:
            self.isScreenMaximized=True
            icon=QPixmap("icons/arrow-down-left.svg")
            self.animate_maximization=QPropertyAnimation(self,b'geometry')
            self.animate_maximization.setDuration(100)
            self.animate_maximization.setStartValue(self.geometry())
            self.animate_maximization.setEndValue(self.desktop.screenGeometry())
            self.animate_maximization.start()

        icon=QIcon(icon)

        self.maximize_btn.setIcon(icon)

    def open_url(self,link):
        link=QUrl(link)
        QDesktopServices.openUrl(link)
        


    def doStyling(self):

        toggle=QPixmap("icons/align-left.svg")
        toggle = QIcon(toggle)
        self.toggle_sidebar.setIcon(toggle)
        # self.toggle_sidebar.setIconSize(self.toggle_sidebar.size())
        self.toggle_sidebar.setCursor(Qt.PointingHandCursor)

        minimize=QPixmap("icons/minus.svg")
        minimize=QIcon(minimize)
        self.minimize_btn.setIcon(minimize)

        maximize=QPixmap("icons/arrow-up-right.svg")
        maximize=QIcon(maximize)
        self.maximize_btn.setIcon(maximize)

        close=QPixmap("icons/x.svg")
        close=QIcon(close)
        self.close_btn.setIcon(close)

        github=QPixmap("icons/github.svg")
        github=QIcon(github)
        self.github_link_btn.setIcon(github)
        self.github_link_btn.setCursor(Qt.PointingHandCursor)

        linkedin=QPixmap("icons/linkedin.svg")
        linkedin=QIcon(linkedin)
        self.linkedin_link_btn.setIcon(linkedin)
        self.linkedin_link_btn.setCursor(Qt.PointingHandCursor)

        self.visualize_data_btn.setCursor(Qt.PointingHandCursor)
        self.view_data_btn.setCursor(Qt.PointingHandCursor)
        self.another_btn.setCursor(Qt.PointingHandCursor)

        # visualized_icon=QPixmap("icons/data_visualization_icon.jpg")
        visualized_icon=QPixmap("icons/data_visualization_icon_1.png")
        visualized_btn=QPushButton(QIcon(visualized_icon),"")
        visualized_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        visualized_btn.setObjectName("visualized_btn")
        # visualized_btn.setIconSize(QSize(1000,1000))
        self.layout_on_body_frame.addWidget(visualized_btn)

        # print(self.body_frame.geometry())


    # override the mouseEvents to make movement of the screen possible

    def mousePressEvent(self,event):
        """previous position"""
        self.previous_pos=event.globalPos()

    
    def mouseMoveEvent(self,event):
        """new position"""
        new_pos=QPoint(event.globalPos()-self.previous_pos)
        self.move(self.x()+new_pos.x(),self.y()+new_pos.y())
        self.previous_pos=event.globalPos()

    def closeEvent(self,event):
        # store.print()
        store.close()
        event.accept()



if __name__=="__main__":
    app=QApplication(sys.argv)
    window=MainWindow()
    window.show()
    sys.exit(app.exec_())