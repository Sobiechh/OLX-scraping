import pandas as pd

class DataManage:
    def __init__(self):
        self._df = pd.DataFrame()
    
    def save_data(self, documents):
        df = pd.DataFrame().from_records(documents)
        df.drop_duplicates(subset=['id'], inplace=True)

        df.to_excel('data.xlsx', index=False)