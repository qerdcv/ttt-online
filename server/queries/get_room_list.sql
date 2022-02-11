SELECT id, name, is_private
FROM rooms
ORDER BY count LIMIT $2 OFFSET $1;
