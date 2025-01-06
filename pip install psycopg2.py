import requests

# Your Riot API Key
API_KEY = "RGAPI-291d27e2-d784-4a8f-ba31-d9152a55ecdb"

# Base headers for API requests
HEADERS = {
    "X-Riot-Token": API_KEY
}


def get_summoner_info(region, summoner_name, tag):
    url = f"https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{summoner_name}/{tag}?api_key={API_KEY}"

    response = requests.get(url, headers=HEADERS)
    print(response.text)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.json()}")
        return None

# Example usage
region = "americas"  # Change to your region
summoner_name = "Shiyo"
tag = "NA1"
summoner_info = get_summoner_info(region, summoner_name, tag)
puuid = summoner_info["puuid"]


def get_match_history(region, puuid, count=5):
    url = f"https://{region}.api.riotgames.com/tft/match/v1/matches/by-puuid/{puuid}/ids?start=0&count=1000&api_key={API_KEY}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.json()}")
        return None

# Example usage
match_history = get_match_history(region, puuid, count=5)
if match_history:
    print("Match History:", match_history)

def get_match_details(region, match_id):
    url = f"https://{region}.api.riotgames.com/tft/match/v1/matches/{match_id}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.json()}")
        return None

# Example usage
# if match_history:
#     for match_id in match_history:
#         match_details = get_match_details(region, match_id)
#         if match_details:
#             print(f"Match Details for {match_id}:", match_details)
