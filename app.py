from flask import Flask, request, jsonify
from api import RiotAPI
from database import connections

def analyze_performance(cursor, puuid):
    """
    Analyze the player's performance based on match data in the database.
    
    Args:
        cursor: Database cursor object.
        puuid: The player's unique identifier.

    Returns:
        A dictionary containing performance metrics.
    """
    # Fetch participant data for the player's PUUID
    cursor.execute("""
        SELECT placement, total_damage_to_players
        FROM Participants
        WHERE puuid = %s
    """, (puuid,))
    results = cursor.fetchall()

    if not results:
        return {"error": "No data found for the specified player"}

    # Calculate performance metrics
    placements = [row[0] for row in results]
    damages = [row[1] for row in results]

    avg_placement = sum(placements) / len(placements)
    first_place_wins = placements.count(1)
    total_damage = sum(damages)

    return {
        "average_placement": avg_placement,
        "first_place_wins": first_place_wins,
        "total_damage": total_damage
    }

app = Flask(__name__)

# Initialize Riot API and Database
api_key = "RGAPI-f245a814-3301-4ccc-b4fc-63e425a9f209"
region = "americas"
riot_api = RiotAPI(api_key, region)

@app.route('/api/analyze', methods=['GET'])
def analyze_summoner():
    summoner_name = request.args.get('summoner')
    tag = request.args.get('tag')

    if not summoner_name or not tag:
        return jsonify({"error": "Summoner name and tag are required"}), 400

    # Fetch Summoner Info
    summoner_info = riot_api.get_summoner_info(summoner_name, tag)
    if not summoner_info:
        return jsonify({"error": "Summoner not found"}), 404

    puuid = summoner_info["puuid"]

    # Fetch Match History
    match_history = riot_api.get_match_history(puuid, count=5)
    if not match_history:
        return jsonify({"error": "No match history found"}), 404

    # Analyze Performance
    db = connections.TFTDatabase(
        dbname="tft_analyzer",
        user="postgres",
        password="your_password",
        host="localhost",
        port=5432
    )

    
    performance = analyze_performance(db.cursor, puuid)
    db.close_connection()

    return jsonify(performance)

if __name__ == '__main__':
    app.run(debug=True)
