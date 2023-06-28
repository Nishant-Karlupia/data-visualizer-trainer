import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication,QMainWindow,QWidget,QPushButton,QComboBox,QCheckBox,QFormLayout,QDockWidget,QTableView,QHeaderView,QGraphicsView
from PyQt5.QtChart import QChart,QChartView,QLineSeries,QValueAxis
from PyQt5.QtGui import QPainter,QColor,QStandardItemModel,QStandardItem
from random import randint as rand
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt
from CustomWidgets import ChartView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        self.setMinimumSize(1200,600)
        self.setWindowTitle("Data Visualization")
        self.setupChart()
        self.setupToolsDockWidget()
        self.setupMenu()
        # self.loadCSVFile()
        self.show()

    def setupChart(self):
        

        self.model=QStandardItemModel()
        self.model.setColumnCount(3)
        self.model.setHorizontalHeaderLabels(['Year','Socail Exp',"Country"])

        data_and_labels=self.loadCSVFile()
        x_values,y_values,labels=[],[],[]

        for item in range(len(data_and_labels)):
            x_values.append(data_and_labels[item][0])
            y_values.append(data_and_labels[item][1])
            labels.append(data_and_labels[item][2])

        # labels_set=list(set(tuple(labels)))
        # print(labels)
        # set will not work as it rearranges the ordering of the elements and hence it could cause problem when inserting the data in the model
        labels_set=[]
        [labels_set.append(x) for x in labels if x not in labels_set]
        # print(labels_set)

        self.chart=QChart()
        self.chart.setTitle("Social Spending")
        self.chart.legend().hide()

        self.axis_x=QValueAxis()
        self.axis_x.setLabelFormat("%i")
        self.axis_x.setTickCount(10)
        self.axis_x.setRange(1880,2016)
        self.chart.addAxis(self.axis_x,Qt.AlignBottom)

        self.axis_y=QValueAxis()
        self.axis_y.setLabelFormat("%i"+"%")
        self.axis_y.setRange(0,40)
        self.chart.addAxis(self.axis_y,Qt.AlignLeft)

        series_dict={}
        for label in labels_set:
            series_label='series_{}'.format(label)
            series_dict[series_label]=label

        # print(series_dict)


        for key in series_dict.keys():
            label=series_dict.get(key)
            line_series=QLineSeries()
            line_series.setName(label)
            line_series.setColor(QColor(rand(10,254),rand(10,254),rand(10,254)))

            for value in range(len(data_and_labels)):
                if line_series.name()==data_and_labels[value][2]:
                    line_series.append(x_values[value],y_values[value])

                    items=[QStandardItem(str(item)) for item in data_and_labels[value]]

                    color=line_series.pen().color()
                    for item in items:
                        item.setBackground(color)

                    # print(value)
                    # print(data_and_labels[value][2]) 
                    self.model.insertRow(value,items)

            # print(line_series.name())
            self.chart.addSeries(line_series)
            line_series.attachAxis(self.axis_x)
            line_series.attachAxis(self.axis_y)

        self.chart_view=ChartView(self.chart)
        self.setCentralWidget(self.chart_view)


    def setupToolsDockWidget(self):
        tools_dock=QDockWidget()
        tools_dock.setWindowTitle("Tools")
        tools_dock.setMinimumWidth(400)
        tools_dock.setAllowedAreas(Qt.LeftDockWidgetArea|Qt.RightDockWidgetArea)

        themes_cb=QComboBox()
        themes_cb.addItems(["Light", "Cerulean Blue", "Dark", "Sand Brown", "NCS Blue", "High Contrast", "Icy Blue", "Qt"])
        themes_cb.currentTextChanged.connect(self.changeChartTheme)

        self.animations_cb=QComboBox()
        self.animations_cb.addItem("No Animation",QChart.NoAnimation)
        self.animations_cb.addItem("Grid Animation",QChart.GridAxisAnimations)
        self.animations_cb.addItem("Series Animation",QChart.SeriesAnimations)
        self.animations_cb.addItem("All Animations",QChart.AllAnimations)

        self.animations_cb.currentIndexChanged.connect(self.changeAnimations)

        self.legend_cb=QComboBox()
        self.legend_cb.addItem("No Legend")
        self.legend_cb.addItem("Align Left",Qt.AlignLeft)
        self.legend_cb.addItem("Align Top",Qt.AlignTop)
        self.legend_cb.addItem("Align Right",Qt.AlignRight)
        self.legend_cb.addItem("Align Bottom",Qt.AlignBottom)
        self.legend_cb.currentTextChanged.connect(self.changeLegend)

        self.antialiasing_cb=QCheckBox()
        self.antialiasing_cb.toggled.connect(self.toggleAntialiasing)

        reset_button=QPushButton("Reset Chart Axes")
        reset_button.clicked.connect(self.resetChartZoom)

        data_table_view=QTableView()
        data_table_view.setModel(self.model)
        data_table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        data_table_view.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        dock_form=QFormLayout()
        dock_form.setAlignment(Qt.AlignTop)
        dock_form.addRow("Themes: ",themes_cb)
        dock_form.addRow("Animations: ",self.animations_cb)
        dock_form.addRow("Legend: ",self.legend_cb)
        dock_form.addRow("Anti-Aliasing: ",self.antialiasing_cb)
        dock_form.addRow(reset_button)
        dock_form.addRow(data_table_view)

        tools_container=QWidget()
        tools_container.setLayout(dock_form)
        tools_dock.setWidget(tools_container)

        self.addDockWidget(Qt.LeftDockWidgetArea,tools_dock)

        self.toggle_dock_tools_act=tools_dock.toggleViewAction()

    
    def changeChartTheme(self,text):
        themes_dict = {"Light": 0, "Cerulean Blue": 1, "Dark": 2, "Sand Brown": 3, "NCS Blue": 4, "High Contrast": 5, "Icy Blue": 6, "Qt": 7}
        theme = themes_dict.get(text)

        if theme==0:
            self.setupChart()

        else:
            self.chart.setTheme(theme)

    def changeAnimations(self):
        animation=QChart.AnimationOptions(self.animations_cb.itemData(self.animations_cb.currentIndex()))
        self.chart.setAnimationOptions(animation)

    def changeLegend(self,text):
        alignment = self.legend_cb.itemData(self.legend_cb.currentIndex())
        if text=='No Legend':
            self.chart.legend().hide()
        else:
            self.chart.legend().setAlignment(Qt.Alignment(alignment))
            self.chart.legend().show()

    def toggleAntialiasing(self,state):
        if state:
            self.chart_view.setRenderHint(QPainter.Antialiasing, on=True)
        else:
            self.chart_view.setRenderHint(QPainter.Antialiasing, on=False)

    def resetChartZoom(self):
        self.chart.zoomReset()
        self.axis_x.setRange(1880,2016)
        self.axis_y.setRange(0,40)


    def setupMenu(self):
        menu_bar=self.menuBar()
        menu_bar.setNativeMenuBar(False)

        view_menu=menu_bar.addMenu('View')
        view_menu.addAction(self.toggle_dock_tools_act)
    
    def loadCSVFile(self):
        filename="social_spending_simplified.csv"

        df=pd.read_csv(filename)

        x_values=list(df['Year'].values)
        y_values=list(df['socialexpendituregdp'].values)
        labels=list(df['Entity'].values)

        data_and_labels=[]

        for item in zip(x_values,y_values,labels):
            data_and_labels.append(list(item))


        return data_and_labels


if __name__=="__main__":
    app=QApplication(sys.argv)
    window=MainWindow()
    sys.exit(app.exec_())