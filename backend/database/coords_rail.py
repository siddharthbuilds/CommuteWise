from database.data_cleaning_electric_train import df_rail
import json
stations = sorted(
    df_rail["Station"]
    .dropna()
    .unique()
)

print(len(stations))
stations = sorted(
    df_rail["Station"]
    .str.replace("\xa0", "", regex=False)
    .str.strip()
    .unique()
)
for station in stations:
    print(station)
chennai_stations_coords = {
    "Ambattur RS": {"latitude": 13.1192, "longitude": 80.1541},
    "Athipattu Pudhunagar RS": {"latitude": 13.2327, "longitude": 80.3168},
    "Athipattu RS": {"latitude": 13.2425, "longitude": 80.3194},
    "Avadi RS": {"latitude": 13.1165, "longitude": 80.0984},
    "Basin Bridge RS": {"latitude": 13.1017, "longitude": 80.2701},
    "Chengalpattu Junction RS": {"latitude": 12.6931, "longitude": 79.9774},
    "Chennai Beach RS": {"latitude": 13.0943, "longitude": 80.2889},
    "Chennai Central MMC": {"latitude": 13.0827, "longitude": 80.2745},
    "Chennai Egmore RS; Rail Terminus": {"latitude": 13.0792, "longitude": 80.2612},
    "Chennai Fort RS": {"latitude": 13.0864, "longitude": 80.2883},
    "Chennai Park RS; Chennai Central": {"latitude": 13.0799, "longitude": 80.2725},
    "Chepauk RS": {"latitude": 13.0645, "longitude": 80.2817},
    "Chetpat RS": {"latitude": 13.0694, "longitude": 80.2443},
    "Chintadripet RS": {"latitude": 13.0745, "longitude": 80.2759},
    "Chromepet RS": {"latitude": 12.9515, "longitude": 80.1411},
    "Ennore RS": {"latitude": 13.2163, "longitude": 80.3228},
    "Greenways Road RS": {"latitude": 13.0214, "longitude": 80.2604},
    "Guduvancheri RS": {"latitude": 12.8427, "longitude": 80.0633},
    "Guindy RS": {"latitude": 13.0084, "longitude": 80.2212},
    "Gummidipoondi RS": {"latitude": 13.4111, "longitude": 80.1232},
    "Hindu College RS": {"latitude": 13.1206, "longitude": 80.0784},
    "Indira Nagar RS": {"latitude": 12.9972, "longitude": 80.2536},
    "Kasthurba Nagar RS": {"latitude": 13.0069, "longitude": 80.2547},
    "Kathivakkam RS": {"latitude": 13.1972, "longitude": 80.3164},
    "Kattangulathur RS": {"latitude": 12.8197, "longitude": 80.0401},
    "Kodambakkam RS": {"latitude": 13.0487, "longitude": 80.2281},
    "Korattur RS": {"latitude": 13.1114, "longitude": 80.1785},
    "Korukkupet RS": {"latitude": 13.1147, "longitude": 80.2746},
    "Kotturpuram RS": {"latitude": 13.0219, "longitude": 80.2464},
    "Light House RS; Marina Beach": {"latitude": 13.0411, "longitude": 80.2767},
    "Mambalam RS; T Nagar": {"latitude": 13.0401, "longitude": 80.2323},
    "Mandaiveli RS": {"latitude": 13.0233, "longitude": 80.2694},
    "Maraimalai Nagar RS": {"latitude": 12.7981, "longitude": 80.0244},
    "Minambakkam RS": {"latitude": 12.9863, "longitude": 80.1818},
    "Minjur RS": {"latitude": 13.2725, "longitude": 80.2625},
    "Mundagakanniamman": {"latitude": 13.0312, "longitude": 80.2678},
    "Nandiambakkam RS": {"latitude": 13.2561, "longitude": 80.3019},
    "Nungambakkam RS": {"latitude": 13.0617, "longitude": 80.2343},
    "Palavanthangal RS": {"latitude": 12.9912, "longitude": 80.1912},
    "Pallavaram RS": {"latitude": 12.9675, "longitude": 80.1492},
    "Paranur RS": {"latitude": 12.7115, "longitude": 79.9958},
    "Park Town RS": {"latitude": 13.0801, "longitude": 80.2739},
    "Pattabiram RS": {"latitude": 13.1232, "longitude": 80.0594},
    "Pattaravakkam RS": {"latitude": 13.1136, "longitude": 80.1654},
    "Perambur Carriage works RS": {"latitude": 13.1075, "longitude": 80.2336},
    "Perambur Loco Works RS": {"latitude": 13.1084, "longitude": 80.2211},
    "Perambur RS": {"latitude": 13.1065, "longitude": 80.2435},
    "Perungalathur RS": {"latitude": 12.9056, "longitude": 80.0919},
    "Perungudi RS": {"latitude": 12.9654, "longitude": 80.2415},
    "Ponneri RS": {"latitude": 13.3242, "longitude": 80.1983},
    "Potheri RS": {"latitude": 12.8231, "longitude": 80.0428},
    "Putlur RS": {"latitude": 13.1328, "longitude": 79.9392},
    "Royapuram RS": {"latitude": 13.1021, "longitude": 80.2918},
    "Saidapet RS": {"latitude": 13.0194, "longitude": 80.2281},
    "Sevvapet RS": {"latitude": 13.1303, "longitude": 79.9672},
    "Singaperumal Koil RS": {"latitude": 12.7636, "longitude": 79.9778},
    "St Thomas Mount RS": {"latitude": 12.9928, "longitude": 80.2001},
    "Tambaram RS": {"latitude": 12.9249, "longitude": 80.1188},
    "Tambaram Sanatorium RS": {"latitude": 12.9366, "longitude": 80.1292},
    "Taramani RS": {"latitude": 12.9772, "longitude": 80.2428},
    "Thirumayilai RS; Cultural Center": {"latitude": 13.0336, "longitude": 80.2692},
    "Thiruninravur RS": {"latitude": 13.1214, "longitude": 80.0278},
    "Thiruvallikeni RS; Marina Beach": {"latitude": 13.0545, "longitude": 80.2789},
    "Thiruvanmiyur RS": {"latitude": 12.9876, "longitude": 80.2491},
    "Tirusulam RS; Airport": {"latitude": 12.9794, "longitude": 80.1741},
    "Tiruvallur RS": {"latitude": 13.1422, "longitude": 79.9111},
    "Tiruvottiyur RS": {"latitude": 13.1594, "longitude": 80.3015},
    "Tondiarpet RS": {"latitude": 13.1206, "longitude": 80.2863},
    "Urapakkam RS": {"latitude": 12.8647, "longitude": 80.0769},
    "V O C Nagar RS": {"latitude": 13.1368, "longitude": 80.2891},
    "Vandalur RS": {"latitude": 12.8892, "longitude": 80.0817},
    "Velacherry RS": {"latitude": 12.9796, "longitude": 80.2211},
    "Veppampattu RS": {"latitude": 13.1245, "longitude": 80.0039},
    "Villivakkam RS": {"latitude": 13.1067, "longitude": 80.2052},
    "Vyasarpadi Jeeva RS": {"latitude": 13.1042, "longitude": 80.2573},
    "Washermanpet RS": {"latitude": 13.0978, "longitude": 80.2796},
    "Wimco Nagar RS": {"latitude": 13.1646, "longitude": 80.3011}
}
rail_nodes = set(df_rail["Station"])

print("Rail nodes:", len(rail_nodes))
print("Rail coords:", len(chennai_stations_coords))

print(
    rail_nodes -
    set(chennai_stations_coords.keys())
)
with open("./database/rail_coords.json", "w") as f:
    json.dump(chennai_stations_coords, f, indent=4)