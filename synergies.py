import networkx as nx
from database import connections # Import your database class
import matplotlib.pyplot as plt

def build_graph(cursor):
    """
    Build a graph representing traits and units.
    """
    G = nx.Graph()

    # Fetch traits and units from the database
    cursor.execute("""
        SELECT DISTINCT Traits.name, Units.character_id
        FROM Traits
        JOIN Units ON Traits.participant_puuid = Units.participant_puuid
    """)
    data = cursor.fetchall()

    # Add edges between traits and units
    for trait, unit in data:
        if not G.has_node(trait):
            G.add_node(trait, type="trait")
        if not G.has_node(unit):
            G.add_node(unit, type="unit")
        G.add_edge(trait, unit)

    return G

def find_clusters(G):
    """
    Find clusters of traits and units.
    """
    clusters = list(nx.connected_components(G))
    return clusters

def recommend_teams(G, cursor):
    """
    Recommend optimal teams based on historical data.
    """
    # Fetch edge weights based on average placement
    cursor.execute("""
        SELECT Traits.name, Units.character_id, AVG(Participants.placement) as avg_placement
        FROM Traits
        JOIN Units ON Traits.participant_puuid = Units.participant_puuid
        JOIN Participants ON Traits.participant_puuid = Participants.puuid
        GROUP BY Traits.name, Units.character_id
    """)
    data = cursor.fetchall()

    # Add weights to edges
    for trait, unit, avg_placement in data:
        if G.has_edge(trait, unit):
            G[trait][unit]['weight'] = avg_placement

    # Find the minimum spanning tree (best combinations)
    mst = nx.minimum_spanning_tree(G, weight='weight')

    return mst

def visualize_graph(G):
    """
    Visualize the trait-unit graph.
    """
    pos = nx.spring_layout(G)
    colors = ['red' if G.nodes[node]['type'] == 'trait' else 'blue' for node in G.nodes()]
    nx.draw(G, pos, with_labels=True, node_color=colors, node_size=500, font_size=10)
    plt.show()

if __name__ == "__main__":
    # Initialize database connection
    db = connections.TFTDatabase(
        dbname="tft_analyzer",
        user="postgres",
        password="your_password",
        host="localhost",
        port=5432
    )

    # Build the graph
    G = build_graph(db.cursor)

    # Find clusters
    clusters = find_clusters(G)
    print("Clusters of Traits and Units:")
    for cluster in clusters:
        print(cluster)

    # Recommend optimal teams
    optimal_teams = recommend_teams(G, db.cursor)
    print("\nRecommended Team Composition:")
    for edge in optimal_teams.edges(data=True):
        print(edge)

    # Visualize the graph
    visualize_graph(G)

    # Close the database connection
    db.close_connection()
