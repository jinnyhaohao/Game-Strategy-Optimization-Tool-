import psycopg2
from psycopg2 import sql, extras
import logging

# Configure logging
logging.basicConfig(
    filename='database.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

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
            logging.info("Database connection established.")
        except Exception as e:
            logging.error(f"Error connecting to the database: {e}")
            raise

    def insert_match_data(self, match_data):
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
                        ",".join(map(str, unit.get("itemNames", [])))  # Handle missing items
                    ))

            # Commit the transaction
            self.conn.commit()
            logging.info(f"Match {match_data['metadata']['match_id']} inserted successfully.")
        except Exception as e:
            logging.error(f"Error inserting match data: {e}")
            self.conn.rollback()  # Rollback in case of error

    def fetch_all_traits(self):
        """
        Fetch all traits from the database.
        """
        try:
            self.cursor.execute("SELECT * FROM Traits")
            traits = self.cursor.fetchall()
            return traits
        except Exception as e:
            logging.error(f"Error fetching traits: {e}")
            return []

    def fetch_all_units(self):
        """
        Fetch all units from the database.
        """
        try:
            self.cursor.execute("SELECT * FROM Units")
            units = self.cursor.fetchall()
            return units
        except Exception as e:
            logging.error(f"Error fetching units: {e}")
            return []

    def fetch_match_by_id(self, match_id):
        """
        Fetch a match by its ID.
        """
        try:
            self.cursor.execute("SELECT * FROM Matches WHERE match_id = %s", (match_id,))
            match = self.cursor.fetchone()
            return match
        except Exception as e:
            logging.error(f"Error fetching match {match_id}: {e}")
            return None

    def delete_match_by_id(self, match_id):
        """
        Delete a match and all related data by match ID.
        """
        try:
            self.cursor.execute("DELETE FROM Traits WHERE match_id = %s", (match_id,))
            self.cursor.execute("DELETE FROM Units WHERE match_id = %s", (match_id,))
            self.cursor.execute("DELETE FROM Participants WHERE match_id = %s", (match_id,))
            self.cursor.execute("DELETE FROM Matches WHERE match_id = %s", (match_id,))
            self.conn.commit()
            logging.info(f"Match {match_id} and related data deleted successfully.")
        except Exception as e:
            logging.error(f"Error deleting match {match_id}: {e}")
            self.conn.rollback()

    def close_connection(self):
        """
        Close the database connection.
        """
        try:
            self.cursor.close()
            self.conn.close()
            logging.info("Database connection closed.")
        except Exception as e:
            logging.error(f"Error closing the database connection: {e}")
