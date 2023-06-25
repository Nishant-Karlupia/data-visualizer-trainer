import sys,csv
import pandas as pd
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication,QWidget,QVBoxLayout
from PyQt5.QtChart import QChart,QChartView,QLineSeries,QValueAxis
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt


class DisplayGraph(QWidget):
    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        self.setMinimumSize(600,400)
        self.setWindowTitle("Simple Line Chart")
        self.setupChart()
        self.show()

    def setupChart(self):
        x_values,y_values=self.loadCSVFile()
        # print(type(x_values),y_values)

        chart=QChart()
        chart.setTitle("Social Spending GDP")
        chart.setAnimationOptions(QChart.SeriesAnimations)
        # chart.legend().hide()
        chart.legend().setAlignment(Qt.AlignRight)
        line_series=QLineSeries()

        for value in range(0,len(x_values)):
            line_series.append(x_values[value],y_values[value])
        chart.addSeries(line_series)

        axis_x=QValueAxis()
        axis_x.setLabelFormat("%i")
        axis_x.setTickCount(10)
        axis_x.setRange(1880,2016)
        chart.addAxis(axis_x,Qt.AlignBottom)
        line_series.attachAxis(axis_x)

        axis_y=QValueAxis()
        axis_y.setLabelFormat("%i"+'%')
        # axis_y.setTickCount(10)
        axis_y.setRange(0,40)
        chart.addAxis(axis_y,Qt.AlignLeft)
        line_series.attachAxis(axis_y)


        chart_view=QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)

        v_box=QVBoxLayout()
        v_box.addWidget(chart_view)
        self.setLayout(v_box)




    def loadCSVFile(self):
        filename="social_spending_simplified.csv"
        df=pd.read_csv(filename)
        x_values=list(df['Year'].values)
        y_values=list(df['socialexpendituregdp'].values)
        # print(x_values)

        return (x_values,y_values)    

if __name__=="__main__":
    app=QApplication(sys.argv)
    window=DisplayGraph()
    sys.exit(app.exec_())