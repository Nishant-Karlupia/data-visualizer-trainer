import sys
import typing
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow,QWidget,QApplication,QVBoxLayout,QTableView,QHeaderView,QLineEdit,QHBoxLayout,QGraphicsDropShadowEffect,QMessageBox,QGridLayout,QLabel,QScrollArea,QStackedWidget,QSizePolicy
from PyQt5.QtGui import QStandardItem,QStandardItemModel
from CustomFunction import Open_Datafile,apply_stylesheet
from CustomWidgets import FirstButton,CustomMessageBox
from globalParams.stateStore import store
from globalParams.dataStore import globalData
import matplotlib.pyplot as plt

class StatisticsWindow(QMainWindow):
    def __init__(self, parent):
        super().__init__(parent)

    # def __init__(self, df):
    #     super().__init__()
        df=parent.dataFrame

        widget=QWidget()
        layout=QVBoxLayout()

        # print(parent.dataFrame)
        # df=df
        
        
        # print(self.dataFrame.describe())
        # print("Data Shape:")
        # print(df.shape)
        # print()

        layout_dtype=QVBoxLayout()
        dtype_data_layout=QGridLayout()

        # Data Types
        data_types = df.dtypes.to_dict()
        data_lst=[]
        # print("Data Types:")
        for column, dtype in data_types.items():
            # print(f"{column}: {dtype}")
            data_lst.append([column,dtype])
        for i in range(len(data_lst)):
            dtype_data_layout.addWidget(QLabel(str(data_lst[i][0])),0,i)
            dtype_data_layout.addWidget(QLabel(str(data_lst[i][1])),1,i)

        dtype_label=QLabel("Data types")
        dtype_label.setObjectName("heading")
        dtype_label.setAlignment(Qt.AlignCenter)
        layout_dtype.addWidget(dtype_label)
        layout_dtype.addLayout(dtype_data_layout)




        # # Unique Values
        # print("Unique Values:")
        # print(type(df.nunique()))
        # print(df.nunique().to_dict())
        # print()
        layout_unique=QVBoxLayout()
        unique_val_layout=QGridLayout()
        unique_data = df.nunique().to_dict()
        data_lst=[]
        # print("Data Types:")
        for column, data in unique_data.items():
            data_lst.append([column,data])
        for i in range(len(data_lst)):
            unique_val_layout.addWidget(QLabel(str(data_lst[i][0])),0,i)
            unique_val_layout.addWidget(QLabel(str(data_lst[i][1])),1,i)

        nunique_label=QLabel("Unique Values")
        nunique_label.setObjectName("heading")
        nunique_label.setAlignment(Qt.AlignCenter)
        layout_unique.addWidget(nunique_label)
        layout_unique.addLayout(unique_val_layout)


        # # Missing Values
        # print("Missing Values:")
        # print(df.isnull().sum())
        # print()

        layout_missing=QVBoxLayout()
        missing_val_layout=QGridLayout()
        missing_data = df.isnull().sum().to_dict()
        data_lst=[]
        for column, data in missing_data.items():
            data_lst.append([column,data])
        for i in range(len(data_lst)):
            missing_val_layout.addWidget(QLabel(str(data_lst[i][0])),0,i)
            missing_val_layout.addWidget(QLabel(str(data_lst[i][1])),1,i)

        missing_label=QLabel("Missing Values")
        missing_label.setObjectName("heading")
        missing_label.setAlignment(Qt.AlignCenter)

        layout_missing.addWidget(missing_label)
        layout_missing.addLayout(missing_val_layout)




        # # Summary Statistics
        # print("Summary Statistics:")
        # print(df.describe().to_dict())
        # print()

        layout_summary=QVBoxLayout()
        summary_data_layout=QGridLayout()
        metrices=['count','mean','std','min','max','25%','50%','75%']
        summary_data=df.describe().to_dict()
        for i in range(len(metrices)):
            summary_data_layout.addWidget(QLabel(metrices[i]),i+1,0)
        col=1
        for column,data in summary_data.items():
            summary_data_layout.addWidget(QLabel(str(column)),0,col)
            for i in range(len(metrices)):
                summary_data_layout.addWidget(QLabel(str(round(data[metrices[i]],2))),i+1,col)
            col+=1

        summary_label=QLabel("Summary")
        summary_label.setObjectName("heading")
        summary_label.setAlignment(Qt.AlignCenter)
        layout_summary.addWidget(summary_label)
        layout_summary.addLayout(summary_data_layout)

        # correlation
        numeric_columns = df.select_dtypes(include='number').columns
        correlation_df = df[numeric_columns]

        # Compute correlation
        correlation_matrix = correlation_df.corr().to_dict()
        corr_keys=list(correlation_matrix.keys())
        # print("Correlation:")
        # print(correlation_matrix)
        # print(corr_keys)
        # print()
        layout_corr=QVBoxLayout()
        corr_data_layout=QGridLayout()
        
        for i in range(len(corr_keys)):
            corr_data_layout.addWidget(QLabel(corr_keys[i]),i+1,0)
            corr_data_layout.addWidget(QLabel(corr_keys[i]),0,i+1)

        for row in range(len(corr_keys)):
            for col in range(len(corr_keys)):
                corr_data_layout.addWidget(QLabel(str(round(correlation_matrix[corr_keys[row]][corr_keys[col]],5))),row+1,col+1)

        corr_label=QLabel("Correlation Summary")
        corr_label.setObjectName("heading")
        corr_label.setAlignment(Qt.AlignCenter)
        layout_corr.addWidget(corr_label)
        layout_corr.addLayout(corr_data_layout)


        layout.addLayout(layout_dtype)
        layout.addLayout(layout_unique)
        layout.addLayout(layout_missing)
        layout.addLayout(layout_summary)
        layout.addLayout(layout_corr)


        widget.setLayout(layout)

        self.setCentralWidget(widget)

        apply_stylesheet(self,'styles/statistics.qss')


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.dataFrame=globalData.give_data()

        self.setWindowTitle("Show the data")
        self.setMinimumSize(500,500)
        self.msg_box=None
        # self.new_data_frame_calcul

        self.open_btn=FirstButton("Open File","open_btn",self.open_file)
                
        self.sep=QLineEdit()
        self.sep.setPlaceholderText("Enter the separator (; , ...etc)")
        self.sep.setObjectName("separator")

        self.model=QStandardItemModel()
        table=QTableView()
        table.setModel(self.model)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        hbox=QHBoxLayout()
        hbox.addWidget(self.open_btn)
        hbox.addWidget(self.sep)

        self.statistics_btn=FirstButton("Show Statistics","statistics",self.set_statistics_layout)
        self.statistics_btn.setDisabled(True)

        
        layout=QVBoxLayout()
        layout.addLayout(hbox)
        layout.addWidget(table)
        layout.addWidget(self.statistics_btn)
        self.model_widget=QWidget()
        self.model_widget.setLayout(layout)

        self.stat_widget=QWidget()
        self.stat_widget_layout=QVBoxLayout()
        self.stat_widget.setLayout(self.stat_widget_layout)

        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(self.model_widget)
        self.stacked_widget.addWidget(self.stat_widget)

        self.stacked_widget.setCurrentWidget(self.model_widget)

        apply_stylesheet(self,'styles/data_model.qss')
        self.show_model_function()


        self.setCentralWidget(self.stacked_widget)

    def open_file(self):

        res=Open_Datafile(self,self.sep)

        if res[0]==None:# no file opened
            return

        if res[0]==False:# file not an excel or csv
            self.msg_box=CustomMessageBox("Error","Make sure that file is .xlsx or .csv")
            store.add(self.msg_box)
            self.msg_box.show()
            return
        
        self.dataFrame=res[1]   
        self.statistics_btn.setDisabled(False)

        self.show_model_function()

    def show_model_function(self):

        if self.dataFrame is None:
            return
        
        

        # # Data Distribution (Histograms)
        # print("Data Distribution:")
        # for column in df.select_dtypes(include='number').columns:
        #     df[column].plot(kind='hist')
        #     plt.title(column)
        #     plt.show()

        # # Categorical Variables (Bar Plots)
        # print("Categorical Variables:")
        # for column in df.select_dtypes(include='object').columns:
        #     df[column].value_counts().plot(kind='bar')
        #     plt.title(column)
        #     plt.show()

        # # Data Preview
        # print("Data Preview (First 5 Rows):")
        # print(df.head())

        globalData.assign_data(self.dataFrame)
        columns=list(self.dataFrame.columns)
        # print(columns)
        self.model.setColumnCount(len(columns))
        self.model.setHorizontalHeaderLabels(columns)

        for ind,value in enumerate(self.dataFrame.values):
            # print(df.value)
            items=[QStandardItem(str(val)) for val in value]
            self.model.insertRow(ind,items)

        
    def set_model_layout(self):
        self.stacked_widget.setCurrentWidget(self.model_widget)



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

    def set_statistics_layout(self):

        self.clear_layout(self.stat_widget_layout)

        self.stat_window=StatisticsWindow(self)


        scroll_area=QScrollArea()
        scroll_area.setWidget(self.stat_window)
        scroll_area.setWidgetResizable(True)


        self.stat_widget_layout.addWidget(scroll_area)
        show_model_btn=FirstButton("show data","show_data",self.set_model_layout)
        self.stat_widget_layout.addWidget(show_model_btn)


        self.stacked_widget.setCurrentWidget(self.stat_widget)

    def closeEvent(self, event):
        store.close()

    

if __name__=="__main__":
    app=QApplication(sys.argv)
    window=MainWindow()
    window.show()
    sys.exit(app.exec_())