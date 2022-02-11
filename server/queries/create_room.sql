INSERT INTO rooms(name, is_private, password)
VALUES ($1, $2, $3)
RETURNING id;
