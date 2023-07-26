import pandas as pd
from PyQt5.QtWidgets import QFileDialog

def Open_Datafile(self,sepLineEdit):
    # return value is tuple (,): so that comparison of return can be done
    # if dataFrame is returned if(dataFrame) is meaningless (truth value required)
    # first value of tuple indicates the success/failure: if success second value is dataFrame

    filename,_=QFileDialog.getOpenFileName(self,"Open File","","All Files(*)")
    if filename:
        get,dataFrame=False,None
        sep=sepLineEdit.text()
        if filename.endswith(".csv"):
            if len(sep)>0:
                dataFrame=pd.read_csv(filename,sep=sep)
            else:
                dataFrame=pd.read_csv(filename)
            get=True
        if filename.endswith(".xlsx"):
            if len(sep)>0:
                dataFrame=pd.read_excel(filename,sep=sep)
            else:
                dataFrame=pd.read_excel(filename)
            get=True
        
        if not get:
            # file not an excel or csv file
            return (False,None)
        
        return (True,dataFrame)
    else:
        # no file selected or opened
        return (None,None)


def apply_stylesheet(self,path):
    # open the .qss file and apply it to the parent window that inherit it

    stylesheet=None
    with open(path, 'r') as f:
        stylesheet = f.read()
    f.close()
    try:
        self.setStyleSheet(stylesheet)
    except:
        pass

