import requests

class RiotAPI:
    def __init__(self, api_key, region="americas"):
        """
        Initialize the RiotAPI class with an API key and default region.
        """
        self.api_key = api_key
        self.region = region
        self.headers = {
            "X-Riot-Token": self.api_key
        }

    def get_summoner_info(self, summoner_name, tag, region=None):
        """
        Fetch summoner information by Riot ID.
        region: Optional region override. Defaults to the class's region.
        """
        # Use the provided region or the default region
        region = region or self.region
        url = f"https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{summoner_name}/{tag}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return None

    def get_match_history(self, puuid, count=100):
        """
        Fetch the match history for a given PUUID.
        """
        url = f"https://{self.region}.api.riotgames.com/tft/match/v1/matches/by-puuid/{puuid}/ids?start=0&count={100}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return None

    def get_match_details(self, match_id):
        """
        Fetch details for a specific match.
        """
        url = f"https://{self.region}.api.riotgames.com/tft/match/v1/matches/{match_id}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return None
