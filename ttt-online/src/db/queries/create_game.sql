WITH g AS ( INSERT INTO games (owner_id) VALUES ($1) RETURNING * )
SELECT
    g.*,
    ow.username AS owner_name,
    op.username AS opponent_name,
    win.username AS winner_name,
    cp.username AS current_player_name
FROM g
LEFT JOIN users ow ON ow.id = g.owner_id
LEFT JOIN users op ON op.id = g.opponent_id
LEFT JOIN users win ON win.id = g.winner_id
LEFT JOIN users cp ON cp.id = g.current_player_id;
