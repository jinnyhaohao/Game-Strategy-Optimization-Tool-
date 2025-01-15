import networkx as nx
from database import connections  # Import your database class

def build_unit_graph(cursor):
    """
    Build a graph representing unit synergies.
    """
    G = nx.Graph()

    # Fetch unit pair performance data from the database
    cursor.execute("""
        SELECT u1.character_id AS unit1, u2.character_id AS unit2, AVG(p.placement) AS avg_placement
        FROM Units u1
        JOIN Units u2 ON u1.match_id = u2.match_id AND u1.participant_puuid = u2.participant_puuid
        JOIN Participants p ON u1.participant_puuid = p.puuid
        WHERE u1.character_id < u2.character_id  -- Avoid duplicate pairs
        GROUP BY u1.character_id, u2.character_id
    """)
    data = cursor.fetchall()

    # Add nodes and edges to the graph
    for unit1, unit2, avg_placement in data:
        if not G.has_node(unit1):
            G.add_node(unit1, type="unit")
        if not G.has_node(unit2):
            G.add_node(unit2, type="unit")
        G.add_edge(unit1, unit2, weight=avg_placement)

    return G

def recommend_unit_pairs(G, top_n=5):
    """
    Recommend the top N unit pairs with the best synergy.
    """
    # Sort edges by weight (ascending: lower avg_placement = better performance)
    sorted_edges = sorted(G.edges(data=True), key=lambda edge: edge[2]['weight'])

    # Return the top N pairs
    return sorted_edges[:top_n]

def recommend_top_units(cursor, top_n=5):
    """
    Recommend the top N individual units based on their average placement.
    """
    cursor.execute("""
        SELECT character_id, AVG(placement) AS avg_placement
        FROM Participants
        JOIN Units ON Participants.puuid = Units.participant_puuid
        GROUP BY character_id
        ORDER BY avg_placement ASC
        LIMIT %s
    """, (top_n,))
    data = cursor.fetchall()

    return data

from itertools import combinations
def recommend_unit_combinations_with_strict_diversity(G, top_n=5, combo_size=4):
    """
    Recommend the top N combinations of `combo_size` units with at least two unique units compared to all previous outputs.
    """
    from itertools import combinations

    # Generate all combinations of `combo_size` units from the graph's nodes
    all_combinations = combinations(G.nodes, combo_size)

    # Calculate the average placement (synergy) for each combination
    combo_scores = []
    for combo in all_combinations:
        # Check if all pairs in the combination exist as edges in the graph
        pair_weights = []
        for pair in combinations(combo, 2):  # Generate all pairs from the combination
            if G.has_edge(*pair):
                pair_weights.append(G[pair[0]][pair[1]]['weight'])

        # If all pairs exist, calculate the average placement
        if pair_weights:
            avg_score = sum(pair_weights) / len(pair_weights)
            combo_scores.append((set(combo), avg_score))  # Use `set` for easier comparison

    # Sort by the average placement (ascending: lower is better)
    sorted_combos = sorted(combo_scores, key=lambda x: x[1])

    # Ensure strict diversity by requiring at least two unique units from all selected combinations
    selected_combinations = []
    for combo, avg_placement in sorted_combos:
        if all(len(combo.difference(prev_combo)) >= 2 for prev_combo, _ in selected_combinations):
            selected_combinations.append((combo, avg_placement))
        if len(selected_combinations) == top_n:
            break

    # Convert sets back to lists for better output formatting
    return [(list(combo), avg_placement) for combo, avg_placement in selected_combinations]



# def visualize_unit_graph(G):
#     """
#     Visualize the unit synergy graph.
#     """
#     import matplotlib.pyplot as plt

#     pos = nx.spring_layout(G)
#     edge_weights = [G[u][v]['weight'] for u, v in G.edges]
#     nx.draw(
#         G, pos, with_labels=True, node_color='lightblue', edge_color=edge_weights,
#         width=2.0, edge_cmap=plt.cm.Blues, node_size=500, font_size=10
#     )
#     plt.colorbar(plt.cm.ScalarMappable(cmap=plt.cm.Blues), label="Synergy (avg placement)")
#     plt.show()

if __name__ == "__main__":
    # Initialize database connection
    db = connections.TFTDatabase(
        dbname="tft_analyzer",
        user="postgres",
        password="your_password",
        host="localhost",
        port=5432
    )

    try:
        # Build the unit graph
        G = build_unit_graph(db.cursor)

        # Recommend the top 5 unit pairs
        top_pairs = recommend_unit_pairs(G, top_n=5)
        print("Top Unit Pairs:")
        for unit1, unit2, data in top_pairs:
            print(f"{unit1} + {unit2}: Avg Placement = {data['weight']:.2f}")

        # Recommend the top 5 individual units
        top_units = recommend_top_units(db.cursor, top_n=5)
        print("\nTop Units:")
        for character_id, avg_placement in top_units:
            print(f"{character_id}: Avg Placement = {avg_placement:.2f}")

        # Recommend the top 5 combinations of 5 units
        # Recommend the top 5 combinations of 5 units
        # Recommend the top 5 diverse combinations of 3 units
        top_combinations = recommend_unit_combinations_with_strict_diversity(G, top_n=5, combo_size=4)
        print("\nTop Strictly Diverse Combinations of 3 Units:")
        for combination, avg_placement in top_combinations:
            print(f"Units: {', '.join(combination)} | Avg Placement: {avg_placement:.2f}")

        # # Visualize the graph
        # visualize_unit_graph(G)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the database connection
        db.close_connection()
