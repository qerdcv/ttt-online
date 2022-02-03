INSERT INTO rooms(name, is_private)
VALUES ($1, $2)
RETURNING id;
