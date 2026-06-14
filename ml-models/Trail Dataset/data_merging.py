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