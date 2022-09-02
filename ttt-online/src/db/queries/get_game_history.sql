SELECT
    gh.game_id as id,
    gh.owner_id, gh.opponent_id, gh.current_player_id,
    gh.step_count, gh.winner_id, gh.field, gh.current_state,
    owner.username as owner_name,
    opponent.username as opponent_name,
    current_player.username as current_player_name,
    winner.username as winner_name
FROM games_history gh
    LEFT JOIN users owner on owner.id = gh.owner_id
    LEFT JOIN users opponent on opponent.id = gh.opponent_id
    LEFT JOIN users current_player on current_player.id = gh.current_player_id
    LEFT JOIN users winner on winner.id = gh.winner_id
WHERE gh.game_id=$1
ORDER BY gh.id;
