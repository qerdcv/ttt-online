SELECT *
FROM games_with_usernames
ORDER BY id LIMIT $2 OFFSET $1;
