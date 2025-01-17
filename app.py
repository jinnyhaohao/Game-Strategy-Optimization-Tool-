from flask import Flask, request, jsonify
from api import RiotAPI
from database import connections
from flask_cors import CORS
from synergies import (
    build_unit_graph,
    recommend_unit_pairs,
    recommend_top_units,
    recommend_unit_combinations_with_strict_diversity
)
from traits import recommend_top_traits, recommend_trait_combinations_with_strict_diversity
import networkx as nx

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
CORS(app)

# Initialize Riot API and Database
api_key = "RGAPI-ae7970cf-9558-4f1e-a629-bbba8e95503e"
region = "americas"
riot_api = RiotAPI(api_key, region)

@app.route('/recommendations', methods=['GET'])
def get_recommendations():
    """
    Get recommendations for unit pairs, top units, strictly diverse unit combinations,
    top traits, and strictly diverse trait combinations.
    Query Parameters:
    - top_n: Number of recommendations to return (default: 5)
    - combo_size: Number of units in diverse combinations (default: 3)
    """
    try:
        # Query parameters
        top_n = int(request.args.get('top_n', 5))
        combo_size = int(request.args.get('combo_size', 3))

        # Initialize database connection
        db = connections.TFTDatabase(
            dbname="tft_analyzer",
            user="postgres",
            password="your_password",
            host="localhost",
            port=5432
        )

        # Build the unit graph
        G = build_unit_graph(db.cursor)

        # Get recommendations for units
        top_pairs = recommend_unit_pairs(G, top_n=top_n)
        top_units = recommend_top_units(db.cursor, top_n=top_n)
        diverse_combinations = recommend_unit_combinations_with_strict_diversity(G, top_n=top_n, combo_size=combo_size)

        # Get recommendations for traits
        top_traits = recommend_top_traits(db.cursor, top_n=top_n)
        diverse_trait_combinations = recommend_trait_combinations_with_strict_diversity(db.cursor, top_n=top_n, combo_size=combo_size)

        # Format the response
        response = {
            "unit_recommendations": {
                "top_unit_pairs": [
                    {"unit1": pair[0], "unit2": pair[1], "avg_placement": pair[2]['weight']}
                    for pair in top_pairs
                ],
                "top_units": [
                    {"unit": unit[0], "avg_placement": unit[1]} for unit in top_units
                ],
                "strictly_diverse_combinations": [
                    {"units": combination, "avg_placement": avg_placement}
                    for combination, avg_placement in diverse_combinations
                ]
            },
            "trait_recommendations": {
                "top_traits": [
                    {"trait": trait[0], "avg_placement": trait[1]} for trait in top_traits
                ],
                "strictly_diverse_combinations": [
                    {"traits": combination, "avg_placement": avg_placement}
                    for combination, avg_placement in diverse_trait_combinations
                ]
            }
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if 'db' in locals():
            db.close_connection()

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
    match_history = riot_api.get_match_history(puuid, count=100)
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
