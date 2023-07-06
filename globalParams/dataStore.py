class GlobalDataFrame:
    def __init__(self):
        self.dataFrame=None

    def give_data(self):
        return self.dataFrame
    
    def assign_data(self,data):
        self.dataFrame=data

globalData=GlobalDataFrame()