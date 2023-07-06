import sys
import typing
from PyQt5.QtCore import QObject, Qt,QThread,pyqtSignal
from PyQt5.QtWidgets import QMainWindow,QWidget,QApplication,QVBoxLayout,QLineEdit,QHBoxLayout,QMessageBox,QLabel,QGridLayout,QFrame,QTextEdit
from CustomWidgets import CustomListWidget,FirstButton,CustomMessageBox
from CustomFunction import apply_stylesheet,Open_Datafile
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error,mean_absolute_error,r2_score
from globalParams.stateStore import store


class Worker(QThread):

    matrix=pyqtSignal(dict)

    def __init__(self,x_train,y_train,x_test,y_test):
        super().__init__()
        self.x_train=x_train
        self.y_train=y_train
        self.x_test=x_test
        self.y_test=y_test

    def run(self):
        reg=LinearRegression()
        reg.fit(self.x_train,self.y_train)
        y_pred=reg.predict(self.x_test)
        mse=mean_squared_error(self.y_test,y_pred)
        mae=mean_absolute_error(self.y_test,y_pred)
        cod=r2_score(self.y_test,y_pred)
        score=reg.score(self.x_test,self.y_test)

        matrix={
            "Score":round(score,3),
            "Coefficient of determination":round(cod,3),
            "Mean Absolute Error":round(mae,3),
            "Mean Squared Error":round(mse,3)
        }

        self.matrix.emit(matrix)
        # self.matrix.emit(0)




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

        

        self.confirm_btn=FirstButton("OK","confirm_btn",lambda: self.work_done(x_col,y_col))
        self.close_btn=FirstButton("Close","close_btn",self.close)
        

        widget=QWidget()
        layout=QVBoxLayout()

        item_layout=QGridLayout()

        item_layout.addWidget(train_label,0,0)
        item_layout.addWidget(self.list1,1,0)
        item_layout.addWidget(target_label,0,1)
        item_layout.addWidget(self.list2,1,1)

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

       
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.df,self.data_split,self.x_col,self.y_col=None,None,[],[]
        self.msg_box=None

        self.setWindowTitle("Model Trainig")
        self.setMinimumSize(500,500)

        widget=QWidget()
        self.open_btn=FirstButton("Open File","open_btn",self.open_file)
        
        
        self.sep=QLineEdit()

        self.sep.setPlaceholderText("Enter the separator (; , ...etc)")
        self.sep.setObjectName("separator")


        frame=QFrame()
        self.train_btn=FirstButton("Train","train_btn",self.train_model_function)
        # self.train_btn.setDisabled(True)
        self.train_report=QTextEdit()
        self.train_report.setReadOnly(True)
        self.train_report.setText("No data available")
        self.train_report.setObjectName("train_report")
        frame_layout=QVBoxLayout()
        frame_layout.addWidget(self.train_report)
        frame_layout.addWidget(self.train_btn)
        frame_layout.setAlignment(self.train_btn, Qt.AlignHCenter)
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
        if(len(self.x_col)!=0 and len(self.y_col)!=0):
            print(self.x_col)
            print(self.y_col)

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
            
        self.x_col,self.y_col=[],[]
        
        self.data_split=SplitWindow(list(self.df.columns),self.x_col,self.y_col)
        store.add(self.data_split)
        self.data_split.show()

    
    def train_model_function(self):
        # print("hello world")
        if len(self.x_col)==0 or len(self.y_col)==0:
            return
        
        X,y=self.df[list(self.x_col)],self.df[list(self.y_col)]
        # print(X)
        # print(y)
        x_train,x_test,y_train,y_test=train_test_split(X,y,test_size=0.3)
        
        self.worker=Worker(x_train,y_train,x_test,y_test)
        self.worker.matrix.connect(self.print_report)
        self.worker.start()

        pass

    def print_report(self,matrix):
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