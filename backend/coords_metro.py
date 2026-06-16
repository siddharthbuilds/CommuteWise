from data_cleaning_metro import df
import json
metro_coords = {
    # Blue Line
    "Chennai Airport": (12.9941, 80.1709),
    "Meenambakkam": (12.9814, 80.1793),
    "Nanganallur road": (12.9892, 80.1878),
    "Alandur": (12.9976, 80.2014),
    "Gindy": (13.0084, 80.2212),
    "Liltle mount": (13.0142, 80.2378),
    "Saidapet": (13.0211, 80.2369),
    "Nandanam": (13.0298, 80.2435),
    "Teynampet": (13.0368, 80.2454),
    "AG-DMS": (13.0442, 80.2492),
    "Thousand Lights": (13.0567, 80.2541),
    "LIC": (13.0617, 80.2644),
    "Government Estate": (13.0673, 80.2714),
    "Chennai Central": (13.0815, 80.2728),
    "Highcourt": (13.0864, 80.2858),
    "Manadi": (13.0945, 80.2831),
    "Washermenpet": (13.0978, 80.2796),
    "Sir Theagaraya College": (13.1009, 80.2828),
    "Tondiarpet": (13.1070, 80.2882),
    "New Washermenpet": (13.1118, 80.2917),
    "Tollgate": (13.1219, 80.2952),
    "Kaladipet": (13.1311, 80.2977),
    "Thiruvottiyur": (13.1517, 80.3025),
    "Wimco Nagar": (13.1646, 80.3011),

    # Green Line
    "Egmore": (13.0792, 80.2612),
    "Nehru Park": (13.0793, 80.2491),
    "Kilpauk": (13.0778, 80.2403),  # Kilpauk Medical College
    "Pachaiyappa's College": (13.0771, 80.2289),
    "Shenoy Nagar": (13.0754, 80.2210),
    "Anna Nagar East": (13.0827, 80.2173),
    "Anna Nagar Tower": (13.0847, 80.2112),
    "Thirumangalam": (13.0851, 80.1997),
    "Koyembedu": (13.0734, 80.1951),  # matches your spelling
    "CMBT": (13.0674, 80.2054),
    "Arumbakkam": (13.0617, 80.2117),
    "Vadapalani": (13.0503, 80.2118),
    "Ashok Nagar KK Nagar": (13.0354, 80.2113),
    "Ekkattuthangal": (13.0169, 80.2056),
    "St Thomas Mount": (12.9928, 80.2001)
}
metro_coords["Central Metro"] = metro_coords["Chennai Central"]
metro_nodes = set(df["Station Name"])
metro_coords["Guindy"] = metro_coords.pop("Gindy")
metro_coords["Little Mount"] = metro_coords.pop("Liltle mount")
print(metro_nodes - set(metro_coords.keys()))

with open("metro_coords.json", "w") as f:
    json.dump(metro_coords, f, indent=4)
