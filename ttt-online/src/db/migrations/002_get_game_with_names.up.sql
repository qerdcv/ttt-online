CREATE OR REPLACE VIEW get_games AS
SELECT
    g.*,
    owner.username as owner_name,
    opponent.username as opponent_name,
    current_player.username as current_player_name,
    winner.username as winner_name
FROM games g
LEFT JOIN users owner on owner.id = g.owner_id
LEFT JOIN users opponent on opponent.id = g.opponent_id
LEFT JOIN users current_player on current_player.id = g.current_player_id
LEFT JOIN users winner on winner.id = g.winner_id;
