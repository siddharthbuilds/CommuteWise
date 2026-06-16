import pandas as pd
df=pd.read_csv("chennai_metro_rail_limited_chennai.csv")
extension = pd.DataFrame({
    "City": ["Chennai"] * 7,
    "Zone": [""] * 7,
    "Division": [""] * 7,
    "Corridor Name": ["Corridor 1 Green Line"] * 7,
    "Interchange": [""] * 7,
    "Station Name": [
        "Sir Theagaraya College",
        "Tondiarpet",
        "New Washermenpet",
        "Tollgate",
        "Kaladipet",
        "Thiruvottiyur",
        "Wimco Nagar"
    ],
    "Layout": ["Elevated"] * 7
})
df = pd.concat([df, extension], ignore_index=True)
df["Station Name"] = df["Station Name"].replace({
    "Gindy": "Guindy",
    "Liltle mount": "Little Mount",
    "Ekkattuthanqal": "Ekkattuthangal",
    "Nehru Fark": "Nehru Park"
})