CREATE TABLE IF NOT EXISTS rooms(
    id SERIAL,
    name VARCHAR(27) UNIQUE,
    is_private BOOLEAN,
    password VARCHAR(27) DEFAULT ''
);
