UPDATE games
SET
    owner_id=$2,
    opponent_id=$3,
    current_player_id=$4,
    step_count=$5,
    winner_id=$6,
    field=$7,
    current_state=$8
WHERE id=$1
