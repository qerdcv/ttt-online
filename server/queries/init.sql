CREATE TABLE IF NOT EXISTS rooms(
    id SERIAL,
    name VARCHAR(27),
    is_private BOOLEAN,
    password VARCHAR(27) DEFAULT '',
    game_id INTEGER
);
