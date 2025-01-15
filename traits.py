import networkx as nx
from database import connections  # Import your database class


def recommend_top_traits(cursor, top_n=5):
    """
    Recommend the top N traits based on their average placement.
    """
    cursor.execute("""
        SELECT Traits.name, AVG(Participants.placement) AS avg_placement
        FROM Traits
        JOIN Participants ON Traits.participant_puuid = Participants.puuid
        GROUP BY Traits.name
        ORDER BY avg_placement ASC
        LIMIT %s
    """, (top_n,))
    data = cursor.fetchall()

    return data


def recommend_trait_combinations_with_strict_diversity(cursor, top_n=5, combo_size=3):
    """
    Recommend the top N combinations of `combo_size` traits with strict diversity.
    """
    # Fetch all traits and their average placement
    cursor.execute("""
        SELECT Traits.participant_puuid, ARRAY_AGG(DISTINCT Traits.name) AS traits, AVG(Participants.placement) AS avg_placement
        FROM Traits
        JOIN Participants ON Traits.participant_puuid = Participants.puuid
        GROUP BY Traits.participant_puuid
    """)
    all_combinations_data = cursor.fetchall()

    # Collect valid combinations
    combo_scores = []
    for _, traits, avg_placement in all_combinations_data:
        if len(traits) >= combo_size:
            combo_scores.append((set(traits[:combo_size]), avg_placement))  # Convert traits to set for diversity comparison

    # Sort combinations by average placement
    sorted_combos = sorted(combo_scores, key=lambda x: x[1])

    # Ensure strict diversity by requiring at least two unique traits from previous combinations
    selected_combinations = []
    for combo, avg_placement in sorted_combos:
        if all(len(combo.difference(prev_combo)) >= 2 for prev_combo, _ in selected_combinations):
            selected_combinations.append((combo, avg_placement))
        if len(selected_combinations) == top_n:
            break

    # Convert sets back to lists for output
    return [(list(combo), avg_placement) for combo, avg_placement in selected_combinations]

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
        # Recommend the top 5 traits
        top_traits = recommend_top_traits(db.cursor, top_n=5)
        print("\nTop Traits:")
        for trait_name, avg_placement in top_traits:
            print(f"{trait_name}: Avg Placement = {avg_placement:.2f}")

        # Recommend the top 5 diverse combinations of 3 traits
        top_trait_combinations = recommend_trait_combinations_with_strict_diversity(db.cursor, top_n=5, combo_size=3)
        print("\nTop Strictly Diverse Combinations of 3 Traits:")
        for combination, avg_placement in top_trait_combinations:
            print(f"Traits: {', '.join(combination)} | Avg Placement: {avg_placement:.2f}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the database connection
        db.close_connection()

