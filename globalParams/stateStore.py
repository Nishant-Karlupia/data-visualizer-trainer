class StoreManagement:
    def __init__(self):
        self.open_windows=[]

    def add(self,window):
        self.open_windows.append(window)

    def remove(self,window):
        self.open_windows.remove(window)

    def print(self):
        for win in self.open_windows:
            print(win)
    
    def close(self):
        for window in self.open_windows:
            window.close()
        self.open_windows=[]

store=StoreManagement()
