import sys
import typing
from PyQt5.QtCore import QObject, Qt,QThread,pyqtSignal
from PyQt5.QtWidgets import QMainWindow,QWidget,QApplication,QVBoxLayout,QLineEdit,QHBoxLayout,QMessageBox,QLabel,QGridLayout,QFrame,QTextEdit,QCheckBox,QComboBox
from CustomWidgets import CustomListWidget,FirstButton,CustomMessageBox
from CustomFunction import apply_stylesheet,Open_Datafile
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error,mean_absolute_error,r2_score
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from globalParams.stateStore import store
from globalParams.dataStore import globalData



class Worker(QThread):

    matrix=pyqtSignal(dict)

    def __init__(self,x_train,y_train,x_test,y_test,imputer_columns,scaling_columns,ohe_columns):
        super().__init__()
        self.x_train=x_train
        self.y_train=y_train
        self.x_test=x_test
        self.y_test=y_test
        self.imputer_columns=imputer_columns
        self.scaling_columns=scaling_columns
        self.ohe_columns=ohe_columns

    def run(self):
            print(self.x_train)
            print(self.imputer_columns)
            # print(self.scaling_columns)
            # print(self.ohe_columns)
            print(self.x_train.columns[self.scaling_columns])
            print(self.x_train.columns[self.ohe_columns])
        # try:

            # ************imputers**********
            trf_imputer=ColumnTransformer(self.imputer_columns,remainder='passthrough')

            # ************scaling***********
            trf_scale=ColumnTransformer([
                ('scale',StandardScaler(),self.scaling_columns)
            ],remainder='passthrough')
            # ******************************

            # *****************ohe******************
            trf_ohe=ColumnTransformer([
                ('ohe',OneHotEncoder(sparse_output=False,handle_unknown='ignore'),self.ohe_columns)
            ],remainder='passthrough')
            # **************************************

            # *****************regressor******************
            trf_reg=LinearRegression()
            # trf_reg=DecisionTreeClassifier()
            # ********************************************

            # ***********pipeline*************
            # pipe=Pipeline([
            #     ("trf_imputer",trf_imputer),
            #     ("trf_scale",trf_scale),
            #     ("trf_ohe",trf_ohe),
            #     ("trf_reg",trf_reg)
            # ])
            pipe=Pipeline([
                ("trf_imputer",trf_imputer),
                ("trf_scale",trf_scale),
                ("trf_ohe",trf_ohe),
                ("trf_reg",trf_reg)
            ])

            # ********************************
            # pipe.fit(self.x_train,self.y_train)
            X_train_transformed = pipe.fit_transform(self.x_train,self.y_train)

            # # Transform the test data using the fitted pipeline
            X_test_transformed = pipe.transform(self.x_test)

            
            # y_pred=pipe.predict(self.x_test)
            # mse=mean_squared_error(self.y_test,y_pred)
            # mae=mean_absolute_error(self.y_test,y_pred)
            # cod=r2_score(self.y_test,y_pred)
            # score=pipe.score(self.x_test,self.y_test)

            # matrix={
            #     "Score":round(score,3),
            #     "Coefficient of determination":round(cod,3),
            #     "Mean Absolute Error":round(mae,3),
            #     "Mean Squared Error":round(mse,3)
            # }
            matrix={"A":1}
            self.matrix.emit(matrix)
        # except:
        #     self.matrix.emit({})



class SplitWindow(QMainWindow):
    def __init__(self,columns,x_col,y_col):
        super().__init__()

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setMinimumSize(750,380)

        
        self.list1=CustomListWidget()
        self.list1.addItems(columns)
        self.list1.currentItemChanged.connect(self.data_change_occur)
        train_label=QLabel("Train Variables")
        train_label.setObjectName("train")

        self.list2=CustomListWidget()
        self.list2.currentItemChanged.connect(self.data_change_occur)
        target_label=QLabel("Target Variables")
        target_label.setObjectName("target")

        self.notRequired=CustomListWidget()
        self.notRequired.currentItemChanged.connect(self.data_change_occur)
        nrdatalabel=QLabel("Not Required")
        nrdatalabel.setObjectName("nrdatalabel")


        

        self.confirm_btn=FirstButton("OK","confirm_btn",lambda: self.work_done(x_col,y_col))
        self.close_btn=FirstButton("Close","close_btn",self.close)
        

        widget=QWidget()
        layout=QVBoxLayout()

        item_layout=QGridLayout()

        item_layout.addWidget(train_label,0,0)
        item_layout.addWidget(self.list1,1,0)
        item_layout.addWidget(target_label,0,1)
        item_layout.addWidget(self.list2,1,1)
        item_layout.addWidget(nrdatalabel,0,2)
        item_layout.addWidget(self.notRequired,1,2)

        btn_layout=QHBoxLayout()
        btn_layout.addWidget(self.confirm_btn)
        btn_layout.addWidget(self.close_btn)

        layout.addLayout(item_layout)
        layout.addLayout(btn_layout)

        widget.setLayout(layout)
        self.setCentralWidget(widget)

        apply_stylesheet(self,'styles/split_data.qss')

    def work_done(self,x_col,y_col):
        x_col.clear()
        y_col.clear()
        for i in range(self.list1.count()):
            item=self.list1.item(i)
            x_col.append(item.text())
        for i in range(self.list2.count()):
            item=self.list2.item(i)
            y_col.append(item.text())

        self.confirm_btn.setEnabled(False)

    def data_change_occur(self):
        self.confirm_btn.setEnabled(True)

"""
# imputation transformer
trf1=ColumnTransformer([
    ('impute_age',SimpleImputer(),[2]),
    ('imputer_embarker',SimpleImputer(strategy='most_frequent'),[6])
],remainder='passthrough')
"""




class ProcessingWindow(QMainWindow):
    def __init__(self,dataFrame,imputer_columns,scale_columns,ohe_columns):
        super().__init__()

        self.df=dataFrame
        # print(self.df)
        self.scale_boxes=[]
        self.ohe_boxes=[]
        self.imputer_boxes=[]

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setMinimumSize(750,380)

        self.close_btn=FirstButton("Close","close",self.close)
        self.ok_btn=FirstButton("ok","ok",lambda:self.addColumnIndex(imputer_columns,scale_columns,ohe_columns))
        self.btnlayout=QHBoxLayout()
        self.btnlayout.addWidget(self.ok_btn)
        self.btnlayout.addWidget(self.close_btn)

        
        self.final_layout=QVBoxLayout()
        self.pipeline_layout=QHBoxLayout()

        widget=QWidget()
        # scaling
        scale_layout=QVBoxLayout()
        scale_layout.addWidget(QLabel("Scaling"))

        for item in dataFrame.columns:
            chb=QCheckBox(item)
            self.scale_boxes.append(chb)
            scale_layout.addWidget(chb)

        # ohe hot encoding
        ohe_layout=QVBoxLayout()
        ohe_layout.addWidget(QLabel("OH Encoding"))

        for item in dataFrame.columns:
            chb=QCheckBox(item)
            self.ohe_boxes.append(chb)
            ohe_layout.addWidget(chb)

        # imputators
        impute_layout=QVBoxLayout()
        impute_layout.addWidget(QLabel("Imputators"))

        combotext=["NA","mean","median","most_frequent"]
        for item in dataFrame.columns:
            combo=QComboBox()
            for txt in combotext:
                # combo.addItem(str(item)+" : ( strategy -> {} ) ".format(txt))
                combo.addItem(str(item)+"::{}".format(txt))

            self.imputer_boxes.append(combo)

            impute_layout.addWidget(combo)
        
        


        self.pipeline_layout.addLayout(scale_layout)
        self.pipeline_layout.addLayout(ohe_layout)
        self.pipeline_layout.addLayout(impute_layout)
        
        
        self.final_layout.addLayout(self.pipeline_layout)
        self.final_layout.addLayout(self.btnlayout)

        widget.setLayout(self.final_layout)

        self.setCentralWidget(widget)
    
    def addColumnIndex(self,imputer_columns,scale_columns,ohe_columns):
        for box in self.scale_boxes:
            if box.isChecked():
                scale_columns.append(self.df.columns.get_loc(box.text()))
                # print(self.df.columns.get_loc(box.text()),box.text())
        # print(columns)

        for box in self.ohe_boxes:
            if box.isChecked():
                ohe_columns.append(self.df.columns.get_loc(box.text()))
                

        for box in self.imputer_boxes:
            txt=box.currentText()
            lst=txt.split("::")
            if lst[1]=='NA':
                continue
            
            imputer=(str(lst[0]),SimpleImputer(strategy=lst[1]),[self.df.columns.get_loc(lst[0])])
            imputer_columns.append(imputer)
            # print(imputer)



    def print_text(self):
        for box in self.scale_boxes:
            if box.isChecked():
                print(self.df.columns.get_loc(box.text()),box.text())

    

        


       
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.df,self.data_split,self.x_col,self.y_col=None,None,[],[]
        self.scaling_columns=[]
        self.ohe_columns=[]
        self.imputer_columns=[]

        self.msg_box=None
        self.df=globalData.give_data()

        self.setWindowTitle("Model Trainig")
        self.setMinimumSize(500,500)

        widget=QWidget()
        self.open_btn=FirstButton("Open File","open_btn",self.open_file)
        
        
        self.sep=QLineEdit()

        self.sep.setPlaceholderText("Enter the separator (; , ...etc)")
        self.sep.setObjectName("separator")


        frame=QFrame()
        self.split_btn=FirstButton("Select Train Test","select_train_test_btn",self.open_data_split_window)
        self.process_btn=FirstButton("Process","select_train_test_btn",self.open_data_processing_window)
        self.train_btn=FirstButton("Train","train_btn",self.train_model_function)
        # self.train_btn.setDisabled(True)
        self.train_report=QTextEdit()
        self.train_report.setReadOnly(True)
        if self.df is None:
            self.train_report.setText("No data available")
            self.split_btn.setDisabled(True)
            self.process_btn.setDisabled(True)
        else:
            self.train_report.setText("select train and target variables")
        self.train_report.setObjectName("train_report")
        frame_layout=QVBoxLayout()
        frame_layout.addWidget(self.train_report)
        btn_layout=QHBoxLayout()
        btn_layout.addWidget(self.split_btn)
        btn_layout.addWidget(self.process_btn)
        btn_layout.addWidget(self.train_btn)
        frame_layout.addLayout(btn_layout)
        # frame_layout.setAlignment(self.train_btn, Qt.AlignHCenter)
        frame.setLayout(frame_layout)

        hbox=QHBoxLayout()
        hbox.addWidget(self.open_btn)
        hbox.addWidget(self.sep)
        
        layout=QVBoxLayout()
        layout.addLayout(hbox)
        layout.addWidget(frame)
        widget.setLayout(layout)


        self.setCentralWidget(widget)

        apply_stylesheet(self,'styles/train_models.qss')


    def open_file(self):
        # if(len(self.x_col)!=0 and len(self.y_col)!=0):
        #     print(self.x_col)
        #     print(self.y_col)

        res=Open_Datafile(self,self.sep)

        if res[0]==None:# no file opened
            return
        
        if res[0]==False:# file not an excel or csv file
            # QMessageBox.critical(self,"Error!!!","Make sure that file is .xlsx or .csv")
            self.msg_box=CustomMessageBox("Error","Make sure that file is .xlsx or .csv")
            store.add(self.msg_box)
            self.msg_box.show()
            return
                
        self.df=res[1]
        globalData.assign_data(self.df)
            
        self.x_col,self.y_col=[],[]

        # self.open_data_split_window()
        self.split_btn.setDisabled(False)
        self.process_btn.setDisabled(False)
        self.train_report.setText("Select train and target variables")

    def open_data_processing_window(self):
        # columns=[]
        self.scaling_columns=[]
        self.ohe_columns=[]
        self.imputer_columns=[]
        
        self.data_split=ProcessingWindow(self.df[list(self.x_col)],self.imputer_columns,self.scaling_columns,self.ohe_columns)
        store.add(self.data_split)
        self.data_split.show()


    def open_data_split_window(self):
        
        self.data_split=SplitWindow(list(self.df.columns),self.x_col,self.y_col)
        store.add(self.data_split)
        self.data_split.show()

    def train_model_function(self):
        # print("hello world")
        if len(self.x_col)==0 or len(self.y_col)==0:
            self.insufficient_data_error_msg=CustomMessageBox("InSufficient Data","Either train or target variable missing")
            store.add(self.insufficient_data_error_msg)
            self.insufficient_data_error_msg.show()
            return
        
        X,y=self.df[list(self.x_col)],self.df[list(self.y_col)]
        # print(X)
        # print(y)
        x_train,x_test,y_train,y_test=train_test_split(X,y,test_size=0.3)
        
        self.worker=Worker(x_train,y_train,x_test,y_test,self.imputer_columns,self.scaling_columns,self.ohe_columns)
        self.worker.matrix.connect(self.print_report)
        self.worker.start()

        pass

    def print_report(self,matrix):
        if len(matrix)==0:
            self.trainig_error=CustomMessageBox("Error","Not able to train, check the data fields again!!!")
            store.add(self.trainig_error)
            self.trainig_error.show()
            return
        report=""
        for key,val in matrix.items():
            report+=str(key)+" : "+str(val)+"\n"
            # print(key,val)
        # print(matrix)
        self.train_report.setText(report)



    # close all second-window opened
    def closeEvent(self,event):
        store.close()
    

if __name__=="__main__":
    app=QApplication(sys.argv)
    window=MainWindow()
    window.show()
    sys.exit(app.exec_())


"""
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error,mean_absolute_error,r2_score
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.tree import DecisionTreeClassifier
import pandas as pd

df=pd.read_csv("sample_data/sample.csv")


X_train,X_test,y_train,y_test=train_test_split(df.drop(columns=['Survived','Age']),df['Survived'],test_size=0.2,random_state=42)
trf1=ColumnTransformer([
    ('impute_age',SimpleImputer(),[2]),
    ('imputer_embarker',SimpleImputer(strategy='most_frequent'),[6])
],remainder='passthrough')

# one hot encoding
trf2=ColumnTransformer([
    ('ohe_gender',OneHotEncoder(sparse_output=False,handle_unknown='ignore'),[1,6])
],remainder='passthrough')

trf3=ColumnTransformer([
    ('scale',StandardScaler(),slice(0,10))
])
trf4=DecisionTreeClassifier()

preprocessor = ColumnTransformer([
    ('categorical', Pipeline([
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('encoder', OneHotEncoder(sparse_output=False, handle_unknown='ignore'))
    ]), ['Sex']),
    ('categorical1', Pipeline([
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('encoder', OneHotEncoder(sparse_output=False, handle_unknown='ignore'))
    ]), ['Embarked'])
], remainder='passthrough')

# Final pipeline
pipe = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', DecisionTreeClassifier())
])
pipe.fit(X_train,y_train)



"""