import pandas as pd
from data_cleaning import df
from weather_dataset import weather_df
df['DATE'] = pd.to_datetime(df['DATE'])