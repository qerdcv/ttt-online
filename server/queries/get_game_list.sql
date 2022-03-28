SELECT id, current_state
FROM games
ORDER BY id LIMIT $2 OFFSET $1;
