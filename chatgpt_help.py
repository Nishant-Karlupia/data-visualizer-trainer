

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