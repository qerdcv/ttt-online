CREATE TABLE IF NOT EXISTS users(
    uid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(30) UNIQUE,
    password VARCHAR(255) NOT NULL
);
