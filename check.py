import pandas as pd

df=pd.read_csv("sample_data/sample.csv")

def print_col(col):
    print(df[col].value_counts().to_dict())


s="Embarked"

print_col(s)
