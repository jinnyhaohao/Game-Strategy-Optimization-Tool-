import psycopg2
from psycopg2 import sql, extras

class TFTDatabase:
    def __init__(self, dbname, user, password, host="localhost", port=5432):
        """
        Initialize the connection to the PostgreSQL database.
        """
        try:
            self.conn = psycopg2.connect(
                dbname=dbname,
                user=user,
                password=password,
                host=host,
                port=port
            )
            self.cursor = self.conn.cursor()
            print("Database connection established.")
        except Exception as e:
            print(f"Error connecting to the database: {e}")
            raise

    def insert_match_data(self, match_data):
        """
        Insert match data, participants, traits, and units into the database.
        """
        try:
            # Insert match details
            self.cursor.execute("""
                INSERT INTO Matches (
                    match_id, data_version, game_datetime, game_length, game_version, queue_id, tft_set_number
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (match_id) DO NOTHING
            """, (
                match_data["metadata"]["match_id"],
                match_data["metadata"]["data_version"],
                match_data["info"]["game_datetime"],
                match_data["info"]["game_length"],
                match_data["info"]["game_version"],
                match_data["info"]["queue_id"],
                match_data["info"]["tft_set_number"]
            ))

            # Insert participant details
            for participant in match_data["info"]["participants"]:
                self.cursor.execute("""
                    INSERT INTO Participants (
                        match_id, puuid, placement, level, gold_left, players_eliminated, time_eliminated, total_damage_to_players
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    match_data["metadata"]["match_id"],
                    participant["puuid"],
                    participant["placement"],
                    participant["level"],
                    participant["gold_left"],
                    participant["players_eliminated"],
                    participant["time_eliminated"],
                    participant["total_damage_to_players"]
                ))

                # Insert traits
                for trait in participant["traits"]:
                    self.cursor.execute("""
                        INSERT INTO Traits (
                            match_id, participant_puuid, name, num_units, tier_current, tier_total
                        ) VALUES (%s, %s, %s, %s, %s, %s)
                    """, (
                        match_data["metadata"]["match_id"],
                        participant["puuid"],
                        trait["name"],
                        trait["num_units"],
                        trait["tier_current"],
                        trait["tier_total"]
                    ))

                # Insert units
                for unit in participant["units"]:
                    self.cursor.execute("""
                        INSERT INTO Units (
                            match_id, participant_puuid, character_id, rarity, tier, items
                        ) VALUES (%s, %s, %s, %s, %s, %s)
                    """, (
                        match_data["metadata"]["match_id"],
                        participant["puuid"],
                        unit["character_id"],
                        unit["rarity"],
                        unit["tier"],
                        ",".join(map(str, unit["items"]))  # Convert list to comma-separated string
                    ))

            # Commit the transaction
            self.conn.commit()
            print(f"Match {match_data['metadata']['match_id']} inserted successfully.")
        except Exception as e:
            print(f"Error inserting match data: {e}")
            self.conn.rollback()  # Rollback transaction in case of error

    def close_connection(self):
        """
        Close the database connection.
        """
        try:
            self.cursor.close()
            self.conn.close()
            print("Database connection closed.")
        except Exception as e:
            print(f"Error closing the database connection: {e}")
 