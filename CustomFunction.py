import pandas as pd
from PyQt5.QtWidgets import QFileDialog

def Open_Datafile(self,sepLineEdit):
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
                dataFrame=pd.read_csv(filename)
            get=True
        
        if not get:
            return (False,None)
        
        return (True,dataFrame)
    else:
        return (None,None)


def apply_stylesheet(self,path):
    stylesheet=None
    with open(path, 'r') as f:
        stylesheet = f.read()
    f.close()
    try:
        self.setStyleSheet(stylesheet)
    except:
        pass

