DO $$ BEGIN
    CREATE TYPE STATE as ENUM ('pending', 'in_game', 'done');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

CREATE TABLE IF NOT EXISTS users(
    id SERIAL PRIMARY KEY,
    username VARCHAR(30) UNIQUE,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS games(
    id SERIAL PRIMARY KEY,
    owner_id INTEGER NOT NULL REFERENCES users(id),
    opponent_id INTEGER REFERENCES users(id),
    current_player_id INTEGER REFERENCES users(id),
    step_count INTEGER DEFAULT 0,
    winner_id INTEGER REFERENCES users(id),
    field json DEFAULT '[["", "", ""], ["", "", ""], ["", "", ""]]',
    current_state STATE DEFAULT 'pending',
    next_state STATE DEFAULT 'in_game'
);
