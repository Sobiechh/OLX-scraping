import pandas as pd

class DataManage:
    def __init__(self):
        self._df = pd.DataFrame({})
    
    @property
    def df(self): 
         return self._df
    
    @df.setter 
    def df(self, new_row): 
        if(new_row == {}): 
            raise ValueError("Empty row to append")  
        self._df = self._df.append(new_row, ignore_index=True)
    
    