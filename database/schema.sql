-- Table for storing match details
CREATE TABLE Matches (
    match_id TEXT PRIMARY KEY,
    data_version TEXT,
    game_datetime BIGINT,
    game_length REAL,
    game_version TEXT,
    queue_id INTEGER,
    tft_set_number INTEGER
);

-- Table for storing participants in matches
CREATE TABLE Participants (
    id SERIAL PRIMARY KEY,
    match_id TEXT REFERENCES Matches(match_id),
    puuid TEXT,
    placement INTEGER,
    level INTEGER,
    gold_left INTEGER,
    players_eliminated INTEGER,
    time_eliminated REAL,
    total_damage_to_players INTEGER
);

-- Table for storing traits used by participants
CREATE TABLE Traits (
    id SERIAL PRIMARY KEY,
    match_id TEXT REFERENCES Matches(match_id),
    participant_puuid TEXT,
    name TEXT,
    num_units INTEGER,
    tier_current INTEGER,
    tier_total INTEGER
);

-- Table for storing units owned by participants
CREATE TABLE Units (
    id SERIAL PRIMARY KEY,
    match_id TEXT REFERENCES Matches(match_id),
    participant_puuid TEXT,
    character_id TEXT,
    rarity INTEGER,
    tier INTEGER,
    items TEXT  -- Store item IDs as a comma-separated string
);
