import pandas as pd
from data_cleaning import df
from weather_dataset import weather_df
df['DATE'] = pd.to_datetime(df['DATE'])
weather_df['DATE']=pd.to_datetime(weather_df['DATE'])
df=pd.merge(df,weather_df,on='DATE',how='inner')
print(df.head(10))
print(df.columns)
print(df.shape)
df['weekday'] = df['DATE'].dt.strftime('%a')
print(df.head(10))
print(df.columns)
print(df.shape)
drop1=["DATE",
       "LINE",
       "ORIENTATION",
       "AVGVELOCITY",
       "TRIPDURATION"
       ]
df=df.drop(columns=drop1)
print(df.head(10))
print(df.columns)
print(df.shape)
df=pd.get_dummies(df,columns=["weekday","TIMEOFDAY"])
print(df.head(10))
print(df.columns)
print(df.shape)
y=df["AVGDELAY"]
X=df.drop(columns="AVGDELAY")
