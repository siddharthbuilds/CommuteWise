import pandas as pd
df=pd.read_csv("MIO_DATA.csv")
print(df["AVGDELAY"].describe())
print((df["AVGDELAY"] > 3000).sum())
print((df["AVGDELAY"] < -3000).sum())
print(
    ((df["AVGDELAY"] > 3000) |
     (df["AVGDELAY"] < -3000)).mean() * 100
)
print(df.corr(numeric_only=True)["AVGDELAY"].sort_values(ascending=False))
print(df.groupby("TIMEOFDAY")["AVGDELAY"].mean())
print(df.groupby("RUSHHOUR")["AVGDELAY"].mean())
print(df["DATE"].value_counts().sort_index())
print(
    df.groupby("DATE")["AVGDELAY"]
      .mean()
      .sort_values()
)