-- SELECT * FROM create_game(game_owner_id:=$1);
with g as ( insert into games (owner_id) values ($1) returning * )
select
    g.*,
    ow.username as owner_name,
    op.username as opponent_name,
    win.username as winner_name,
    cp.username as current_player_name
from g
left join users ow on ow.id = g.owner_id
left join users op on op.id = g.opponent_id
left join users win on win.id = g.winner_id
left join users cp on cp.id = g.current_player_id;
