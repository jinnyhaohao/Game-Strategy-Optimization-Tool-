import api

summoner_name = "Shiyo"
tag = "NA1"

summoner_info = api.get_summoner_info("americas", summoner_name, tag)
if summoner_info:
    puuid = summoner_info["puuid"]
    print(f"PUUID for {summoner_name}: {puuid}")
else:
    print("Failed to fetch summoner info.")
