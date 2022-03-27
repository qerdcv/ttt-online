INSERT INTO games(owner_id)
VALUES ($1)
RETURNING *;