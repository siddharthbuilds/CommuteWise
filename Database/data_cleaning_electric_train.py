import pandas as pd

df_rail = pd.read_csv(
    "Sub_Urban_Rail_Chennai_as_on_20_June_2019.csv",
    encoding="latin1"
)


print(df_rail.columns)
print(df_rail.head(20))
print(df_rail[["Connection", "Station"]].head(40))
df_rail["Station"] = (
    df_rail["Station"]
    .str.replace("\xa0", "", regex=False)
    .str.strip()
)
print(df_rail[df_rail["Interchange"].notna()][["Station", "Interchange"]])
print(df_rail["Interchange"].unique())
