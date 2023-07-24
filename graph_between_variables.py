import sys
from PyQt5 import QtGui
import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QMainWindow,QApplication,QComboBox,QVBoxLayout,QHBoxLayout,QLineEdit,QDockWidget,QCheckBox,QFormLayout,QLabel,QMessageBox,QStackedWidget,QFrame
from PyQt5.QtChart import QChart,QValueAxis,QLineSeries,QScatterSeries,QPieSeries,QBarSeries,QBarSet
from PyQt5.QtChart import QChart, QBarSeries, QBarSet, QBarCategoryAxis
from CustomFunction import Open_Datafile,apply_stylesheet
from CustomWidgets import ChartView,FirstButton,CustomMessageBox
from PyQt5.QtGui import QPainter,QFont
from globalParams.stateStore import store
from globalParams.dataStore import globalData


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Graph between variables")
        self.setMinimumSize(1000,600)

        self.dataFrame=globalData.give_data()
        self.first_time_change=True
        self.msg_box=None
        self.current_chart=QChart()

        self.left_layout=QVBoxLayout()
        self.right_layout=QVBoxLayout()

        self.chart_type_combo=QComboBox()
        self.chart_type_combo.setDisabled(True)
        self.chart_type_combo.addItems(['Line Chart','Pie Chart','Bar Chart'])
        self.chart_type_combo.currentTextChanged.connect(self.change_chart_type_widget)

        self.line_combo_first=QComboBox()
        # self.line_combo_first.setMinimumWidth(150)
        self.line_combo_first.currentIndexChanged.connect(self.make_plot)
        
        self.line_combo_second=QComboBox()
        self.line_combo_second.currentIndexChanged.connect(self.make_plot)

    
        self.bar_combo=QComboBox()
        self.bar_combo.currentIndexChanged.connect(self.make_bar_chart)
        self.pie_combo=QComboBox()

        # self.left_layout.addWidget(self.line_combo_first)
        # self.left_layout.addWidget(self.line_combo_second)


        self.open_btn=FirstButton("Open File","open_btn",self.open_file_function)



        self.sep=QLineEdit()
        self.sep.setPlaceholderText("Enter the separator (; , ...etc)")
        self.sep.setObjectName("separator")

        self.right_up=QHBoxLayout()
        self.right_up.addWidget(self.open_btn)
        self.right_up.addWidget(self.sep)
        # left-top-right-bottom
        self.right_layout.setContentsMargins(5,10,0,5)

        # self.chart_view=QChartView()
        # **********************************************
        self.x_min,self.x_max,self.y_min,self.y_max=0,1,0,1
        self.line_chart=QChart() 
        self.line_chart.legend().hide()
        self.line_chart.setTheme(1)
        self.axis_x=QValueAxis()
        self.axis_x.setRange(self.x_min,self.x_max)
        
        self.axis_y=QValueAxis()
        self.axis_y.setRange(self.y_min,self.y_max)

        self.line_chart.addAxis(self.axis_x,Qt.AlignBottom)
        self.line_chart.addAxis(self.axis_y,Qt.AlignLeft)


        self.chart_view=ChartView(self.line_chart)
        self.chart_view.setStyleSheet("background-color: transparent;")

        # ***********************************************

        widget=QWidget()

        right_widget=QWidget()
        right_widget.setObjectName("container")

        self.main_layout=QHBoxLayout()

        self.right_layout.addLayout(self.right_up)
        self.right_layout.addWidget(self.chart_view)
        right_widget.setLayout(self.right_layout)

        # self.main_layout.addLayout(self.left_layout)
        # self.main_layout.addLayout(self.right_layout)
        self.main_layout.addWidget(right_widget)

        self.main_layout.setContentsMargins(0,0,0,0)
        self.main_layout.setSpacing(0)

        widget.setLayout(self.main_layout)

        self.setCentralWidget(widget)

        self.setChartTypeWidget()
        self.setupToolsDockWidget()
        self.setupMenu()

        
        apply_stylesheet(self,'styles/graph.qss')

        self.assign_combobox_values()

    
    def open_file_function(self):

        self.first_time_change=True

        res=Open_Datafile(self,self.sep)

        if res[0]==None:# no file opened
            return

        if res[0]==False:# file not an excel or csv
            self.msg_box=CustomMessageBox("Error","Make sure that file is .xlsx or .csv")
            store.add(self.msg_box)
            self.msg_box.show()
            return
        

        self.dataFrame=res[1]
        globalData.assign_data(self.dataFrame)
        self.chart_type_combo.setDisabled(False)

        self.assign_combobox_values()



    def assign_combobox_values(self):
        if self.dataFrame is None:
            return
        self.line_combo_first.blockSignals(True)
        self.line_combo_first.clear()
        self.line_combo_first.blockSignals(False)
        self.line_combo_second.blockSignals(True)
        self.line_combo_second.clear()
        self.line_combo_second.blockSignals(False)
        self.line_combo_first.addItems(self.dataFrame.columns)
        self.line_combo_second.addItems(self.dataFrame.columns)


        lst=['whole dataFrame']
        dtypes=self.dataFrame.dtypes.to_dict()
        for col,dtype in dtypes.items():
            if str(dtype).lower()=="object":
                # print(col,dtype)
                lst.append(col)

        self.pie_combo.blockSignals(True)
        self.bar_combo.blockSignals(True)
        self.pie_combo.clear()
        self.bar_combo.clear()

        self.pie_combo.addItems(lst)
        self.bar_combo.addItems(lst)
        self.pie_combo.blockSignals(False)
        self.bar_combo.blockSignals(False)


    def make_plot(self):
        if self.first_time_change:
            self.first_time_change=False
            return
        x_dim=self.line_combo_first.currentText()
        y_dim=self.line_combo_second.currentText()

        x_dtype=self.dataFrame[x_dim].dtype
        y_dtype=self.dataFrame[y_dim].dtype

        self.x_min,self.x_max,self.y_min,self.y_max=10**18,-10**18,10**18,-10**18

        # print(x_dim,y_dim)

        line_series=QLineSeries()
        line_series=QScatterSeries()
        

        for x,y in zip(self.dataFrame[x_dim],self.dataFrame[y_dim]):
            if (type(x)!=int and type(x)!=float) or (type(y)!=int and type(y)!=float):
                self.line_chart.removeAllSeries()
                # print(x,y,type(x),type(y))
                return
            self.x_min=min(self.x_min,x)
            self.x_max=max(self.x_max,x)
            self.y_min=min(self.y_min,y)
            self.y_max=max(self.y_max,y)
            line_series.append(x,y)

        

        # print("yes")
        int_types=[int,np.int64,np.int32,np.int16,np.int8]

        self.axis_x=QValueAxis()
        self.axis_x.setRange(self.x_min,self.x_max)
        self.axis_x.setTitleText(str(x_dim))
        self.axis_x.setTitleFont(QFont("consolas",13))
        if x_dtype in int_types:
            self.axis_x.setLabelFormat("%i")

        self.axis_y=QValueAxis()
        self.axis_y.setRange(self.y_min,self.y_max)
        self.axis_y.setTitleText(str(y_dim))
        self.axis_y.setTitleFont(QFont("consolas",13))
        if y_dtype in int_types:
            self.axis_y.setLabelFormat("%i")
            

        self.line_chart=QChart()
        self.line_chart.legend().hide()
        self.line_chart.setTheme(1)
        self.line_chart.addAxis(self.axis_x,Qt.AlignBottom)
        self.line_chart.addAxis(self.axis_y,Qt.AlignLeft)


        self.line_chart.addSeries(line_series)
        line_series.attachAxis(self.axis_x)
        line_series.attachAxis(self.axis_y)
        self.current_chart=self.line_chart

        
        self.refresh_plot()

    
    def refresh_plot(self):

        self.chart_view=ChartView(self.current_chart)
        self.chart_view.setStyleSheet("background-color: transparent;")


        self.left_layout=QVBoxLayout()
        self.right_layout=QVBoxLayout()


        self.sep=QLineEdit()
        self.sep.setPlaceholderText("Enter the seperator")
        self.sep.setObjectName("separator")

        self.right_up=QHBoxLayout()
        self.right_up.addWidget(self.open_btn)
        self.right_up.addWidget(self.sep)


        widget=QWidget()
        self.main_layout=QHBoxLayout()
        right_widget=QWidget()
        right_widget.setObjectName("container")


        self.right_layout.addLayout(self.right_up)
        self.right_layout.addWidget(self.chart_view)

        right_widget.setLayout(self.right_layout)
        
        self.main_layout.addWidget(right_widget)

        widget.setLayout(self.main_layout)        

        self.main_layout.setContentsMargins(0,0,0,0)
        self.main_layout.setSpacing(0)

        self.setCentralWidget(widget)

    
    def setChartTypeWidget(self):
        self.chart_type_stack_widget=QStackedWidget()
        
        self.line_chart_widget=QWidget()
        self.reset_chart_button=FirstButton("Reset Chart Axes","reset_btn",self.resetChartZoom)
        line_chart_layout=QVBoxLayout()
        # line_chart_layout.addWidget(self.chart_type_combo)
        line_chart_layout.addWidget(self.reset_chart_button)
        line_chart_layout.addWidget(self.line_combo_first)
        line_chart_layout.addWidget(self.line_combo_second)
        self.line_chart_widget.setLayout(line_chart_layout)


        self.piechart_widget=QWidget()
        piechart_layout=QVBoxLayout()
        # piechart_layout.addWidget(self.chart_type_combo)
        piechart_layout.addWidget(self.pie_combo)
        self.piechart_widget.setLayout(piechart_layout)


        self.barchart_widget=QWidget()
        barchart_layout=QVBoxLayout()
        # barchart_layout.addWidget(self.chart_type_combo)
        barchart_layout.addWidget(self.bar_combo)
        self.barchart_widget.setLayout(barchart_layout)
        

        self.chart_type_stack_widget.addWidget(self.line_chart_widget)
        self.chart_type_stack_widget.addWidget(self.piechart_widget)
        self.chart_type_stack_widget.addWidget(self.barchart_widget)

        self.chart_type_stack_widget.setCurrentWidget(self.line_chart_widget)
        # self.chart_type_stack_widget.setCurrentWidget(self.piechart_widget)

        self.chart_type_stack_widget.setMaximumHeight(250)

    def change_chart_type_widget(self,chart):
        if chart=="Line Chart":
            self.chart_type_stack_widget.setCurrentWidget(self.line_chart_widget)
            self.make_plot()
        
        elif chart=="Pie Chart":
            self.chart_type_stack_widget.setCurrentWidget(self.piechart_widget)
            self.make_pie_chart()

        else:
            self.chart_type_stack_widget.setCurrentWidget(self.barchart_widget)
            self.make_bar_chart()

    
    def make_pie_chart(self):
        self.pie_chart=QChart()
        pie_series=QPieSeries()

        text=self.pie_combo.currentText()
        # print(text)
        # print(self.dataFrame.nunique().to_dict())

        for key,value in self.dataFrame.nunique().to_dict().items():
            pie_series.append(str(key),int(value))

        self.pie_chart.addSeries(pie_series)

        self.current_chart=self.pie_chart
        self.refresh_plot()

        self.chart_view.setChart(self.pie_chart)

    def make_bar_chart(self):

        
        text=self.bar_combo.currentText()
        # print(text)

        self.bar_chart=QChart()
        self.bar_chart.setTheme(1)
        bar_series=QBarSeries()
        barset=QBarSet("Simple Bar series")
        val=list(self.dataFrame.nunique().to_dict().values())
        if text!='whole dataFrame':
            val=list(self.dataFrame[text].value_counts().to_dict().values())
        barset.append(val)
        bar_series.append(barset)

        self.bar_chart.addSeries(bar_series)

        
        categories = [str(val) for val in list(self.dataFrame.nunique().to_dict().keys())]
        if text!='whole dataFrame':
            categories = [str(val) for val in list(self.dataFrame[text].value_counts().to_dict().keys())]


        axis_x = QBarCategoryAxis()
        axis_x.append(categories)
        self.bar_chart.createDefaultAxes()
        self.bar_chart.setAxisX(axis_x, bar_series)


        self.current_chart=self.bar_chart
        self.refresh_plot()
            

    

        # self.chart_view.setChart(self.bar_chart)


    


    def setupToolsDockWidget(self):
        tools_dock=QDockWidget()
        tools_dock.setWindowTitle("Tools")
        tools_dock.setMinimumWidth(300)
        tools_dock.setMaximumWidth(300)

        tools_dock.setAllowedAreas(Qt.LeftDockWidgetArea|Qt.RightDockWidgetArea)

        themes_cb=QComboBox()
        themes_cb.addItems(["Cerulean Blue","Light", "Dark", "Sand Brown", "NCS Blue", "High Contrast", "Icy Blue", "Qt"])
        themes_cb.currentTextChanged.connect(self.changeChartTheme)
        # themes_cb.setStyleSheet("")

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

        
        dock_form=QFormLayout()
        dock_form.setAlignment(Qt.AlignTop)
        theme_label=QLabel("Themes")
        theme_label.setObjectName("theme_label")
        dock_form.addRow(theme_label,themes_cb)
        # label.setText("Animations: ")
        animation_label=QLabel("Animations: ")
        animation_label.setObjectName("animation_label")
        dock_form.addRow(animation_label,self.animations_cb)
        # dock_form.addRow(QLabel("Legend: "),self.legend_cb)

        aliasing_label=QLabel("Anti-Aliasing: ")
        aliasing_label.setObjectName("aliasing_label")
        dock_form.addRow(aliasing_label,self.antialiasing_cb)
        # dock_form.addChildLayout(self.left_layout)
        # dock_form.addRow(data_table_view)

        dock_form.addRow(self.chart_type_combo)
        dock_form.addRow(QFrame())

        dock_form.addRow(self.chart_type_stack_widget)


        tools_container=QWidget()
        tools_container.setObjectName("tools_container")
        tools_container.setLayout(dock_form)
        tools_dock.setWidget(tools_container)
        # print(tools_dock.width())
        # print(tools_dock.width())

        self.addDockWidget(Qt.LeftDockWidgetArea,tools_dock)

        self.toggle_dock_tools_act=tools_dock.toggleViewAction()

    
    def changeChartTheme(self,text):
        themes_dict = {"Light": 0, "Cerulean Blue": 1, "Dark": 2, "Sand Brown": 3, "NCS Blue": 4, "High Contrast": 5, "Icy Blue": 6, "Qt": 7}
        theme = themes_dict.get(text)

        # self.line_chart.setTheme(theme)
        self.chart_view.chart.setTheme(theme)

    def changeAnimations(self):
        animation=QChart.AnimationOptions(self.animations_cb.itemData(self.animations_cb.currentIndex()))
        print(self.animations_cb.itemData(self.animations_cb.currentIndex()))
        self.chart_view.chart.setAnimationOptions(animation)

    def changeLegend(self,text):
        alignment = self.legend_cb.itemData(self.legend_cb.currentIndex())
        if text=='No Legend':
            self.chart_view.chart.legend().hide()
        else:
            self.chart_view.chart.legend().setAlignment(Qt.Alignment(alignment))
            self.chart_view.chart.legend().show()

    def toggleAntialiasing(self,state):
        if state:
            self.chart_view.setRenderHint(QPainter.Antialiasing, on=True)
        else:
            self.chart_view.setRenderHint(QPainter.Antialiasing, on=False)

    def resetChartZoom(self):
        self.chart_view.chart.zoomReset()
        # print(self.x_min,self.x_max)
        # print(self.y_min,self.y_max)
        self.axis_x.setRange(self.x_min,self.x_max)
        self.axis_y.setRange(self.y_min,self.y_max)

    def setupMenu(self):
        menu_bar=self.menuBar()
        menu_bar.setNativeMenuBar(False)

        view_menu=menu_bar.addMenu('View')
        view_menu.addAction(self.toggle_dock_tools_act)
            
    
    def closeEvent(self,event):
        store.close()



if __name__=='__main__':
    app=QApplication(sys.argv)
    window=MainWindow()
    window.show()
    sys.exit(app.exec_())