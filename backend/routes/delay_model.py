from datetime import datetime
import joblib
import requests
model = joblib.load("random_reg_model.pkl")
def build_features(date, time):
    dt = datetime.strptime(
        f"{date} {time}",
        "%Y-%m-%d %H:%M"
    )
    hour = dt.hour
    weekday = dt.strftime("%a")
    rushhour = int(
        (7 <= hour <= 10) or
        (17 <= hour <= 20)
    )
    morning = int(6 <= hour < 12)
    afternoon = int(12 <= hour < 17)
    evening = int(17 <= hour < 22)
   
    url = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude=13.0827"
    "&longitude=80.2707"
    "&current=temperature_2m,precipitation,rain"
    )
    data = requests.get(url).json()
    current = data["current"]

    temp = current["temperature_2m"]
    precipitation = current["precipitation"]
    rain = current["rain"]

    features = [[
        rushhour,
        temp,
        precipitation,
        rain,
        int(weekday == "Fri"),
        int(weekday == "Mon"),
        int(weekday == "Sat"),
        int(weekday == "Sun"),
        int(weekday == "Thu"),
        int(weekday == "Tue"),
        int(weekday == "Wed"),

        afternoon,
        evening,
        morning
    ]]
    return features

def predict_delay(date, time):
    features = build_features(date, time)
    prediction = model.predict(features)
    return float(prediction[0])
if __name__ == "__main__":
   print(predict_delay("16-06-2026","08:00"))
 