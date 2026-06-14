import pandas as pd
df=pd.read_csv("public_transport_delays.csv")
drop1 = [
    "trip_id",
    "date",
    "route_id",
    "origin_station",
    "destination_station",
    "scheduled_departure",
    "scheduled_arrival",
    "actual_departure_delay_min",
    
    "event_type",
    "event_attendance_est"
    ]
df = df.drop(columns=drop1)
print(df.head())
print(df.columns)
print(df.dtypes)
df["hour"] = pd.to_datetime(df["time"]).dt.hour
df["minute"] = pd.to_datetime(df["time"]).dt.minute
df = df.drop(columns=["time"])
df = pd.get_dummies(df, columns=["transport_type", "season"])
df=df.drop(columns=['transport_type_Tram'])
print(df.head())
print(df.columns)
print(df.dtypes)
df = pd.get_dummies(
    df,
    columns=["weather_condition"],
    drop_first=True)
y=df["actual_arrival_delay_min"]
X=df.drop(columns=["actual_arrival_delay_min"])
print(df["actual_arrival_delay_min"].describe())
print(df["actual_arrival_delay_min"].value_counts().sort_index())
corrs = df.corr(numeric_only=True)["actual_arrival_delay_min"]
print(corrs.sort_values(ascending=False))
print(
    df.corr(numeric_only=True)["delayed"]
    .sort_values(ascending=False)
)