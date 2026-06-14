from location import coords
import requests
import pandas as pd

url = (
    "https://archive-api.open-meteo.com/v1/archive"
    "?latitude=3.4516"
    "&longitude=-76.5320"
    "&start_date=2025-07-31"
    "&end_date=2025-09-05"
    "&daily=temperature_2m_mean,precipitation_sum,rain_sum"
    "&timezone=auto"
)

data = requests.get(url).json()

weather_df = pd.DataFrame({
    "DATE": data["daily"]["time"],
    "TEMP": data["daily"]["temperature_2m_mean"],
    "PRECIPITATION": data["daily"]["precipitation_sum"],
    "RAIN": data["daily"]["rain_sum"]
})
weather_df.to_csv("weather.csv", index=False)