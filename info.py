import api
from database import connections

# Initialize Riot API and database
api_key = "RGAPI-f245a814-3301-4ccc-b4fc-63e425a9f209"
region = "americas"
riot_api = api.RiotAPI(api_key, region)

db = connections.TFTDatabase(
    dbname="tft_analyzer",
    user="postgres",
    password="your_password",
    host="localhost",
    port=5432
)

# Fetch summoner info
summoner_name = "Shiyo"
tag1 = "NA1"

summoner_info = riot_api.get_summoner_info(summoner_name, tag1)
if summoner_info:
    puuid = summoner_info["puuid"]
    print(f"PUUID for {summoner_name}: {puuid}")

    # Fetch match history
    match_history = riot_api.get_match_history(puuid, count=100)
    if match_history:
        print(f"Match IDs: {match_history}")

        # Fetch and store match details
        for match_id in match_history:
            match_details = riot_api.get_match_details(match_id)
            if match_details:
                db.insert_match_data(match_details)
                print(f"Stored match {match_id} in the database.")
            else:
                print(f"Failed to fetch details for match {match_id}.")
    else:
        print("Failed to fetch match history.")
else:
    print("Failed to fetch summoner info.")

# Close the database connection
db.close_connection()
