import pandas as pd
df_rail = pd.read_csv(
    "Sub_Urban_Rail_Chennai_as_on_20_June_2019.csv",
    encoding="latin1"
)
df_rail["Station"] = (
    df_rail["Station"]
    .str.replace("\xa0", "", regex=False)
    .str.strip()
)
south_extension = [
    "Pallavaram RS",
    "Chromepet RS",
    "Tambaram Sanatorium RS",
    "Tambaram RS",
    "Perungalathur RS",
    "Vandalur RS",
    "Urapakkam RS",
    "Guduvancheri RS",
    "Potheri RS",
    "Kattangulathur RS",
    "Maraimalai Nagar RS",
    "Singaperumal Koil RS",
    "Paranur RS",
    "Chengalpattu Junction RS"
]
west_extension = [
    "Avadi RS",
    "Hindu College RS",
    "Pattabiram RS",
    "Thiruninravur RS",
    "Veppampattu RS",
    "Sevvapet RS",
    "Putlur RS",
    "Tiruvallur RS"
]
north_extension = [
    "Athipattu RS",
    "Athipattu Pudhunagar RS",
    "Nandiambakkam RS",
    "Minjur RS",
    "Ponneri RS",
    "Gummidipoondi RS"
]
new_rows = []

for station in south_extension:
    row = {col: None for col in df_rail.columns}
    row["City"] = "Chennai"
    row["Connection"] = "South Line"
    row["Station"] = station
    new_rows.append(row)

for station in west_extension:
    row = {col: None for col in df_rail.columns}
    row["City"] = "Chennai"
    row["Connection"] = "West Line"
    row["Station"] = station
    new_rows.append(row)

for station in north_extension:
    row = {col: None for col in df_rail.columns}
    row["City"] = "Chennai"
    row["Connection"] = "North Line"
    row["Station"] = station
    new_rows.append(row)

df_rail = pd.concat(
    [df_rail, pd.DataFrame(new_rows)],
    ignore_index=True
)
if __name__ == "__main__":
    print(df_rail.columns)
    print(df_rail.head(20))
    print(df_rail[["Connection", "Station"]].head(40))
    print(df_rail[["Connection", "Station"]].tail(30))
    print(df_rail[df_rail["Connection"] == "South Line"][["Station"]].tail(20))
    print(df_rail[df_rail["Connection"] == "West Line"][["Station"]].tail(15))
    print(df_rail[df_rail["Connection"] == "North Line"][["Station"]].tail(15))
