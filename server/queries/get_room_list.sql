SELECT id, name, is_private
FROM rooms
ORDER BY id LIMIT $2 OFFSET $1;
