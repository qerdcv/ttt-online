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



CREATE OR REPLACE FUNCTION create_game(game_owner_id INTEGER)
RETURNS TABLE (
    id int,
    owner_id int,
    opponent_id int,
    current_player_id int,
    step_count int,
    winner_id int,
    field games.field%type,
    current_state games.current_state%type,
    owner_name users.username%type,
    opponent_name users.username%type,
    current_player_name users.username%type,
    winner_name users.username%type
)
language plpgsql
as
$$
DECLARE
    new_game_id INT;
BEGIN
    INSERT INTO games(owner_id) VALUES (game_owner_id) RETURNING games.id INTO new_game_id;
    return QUERY
        SELECT * FROM get_games gg WHERE gg.id=new_game_id;
END
$$;
