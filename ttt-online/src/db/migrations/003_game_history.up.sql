CREATE TABLE IF NOT EXISTS games_history(
   id SERIAL PRIMARY KEY,
   game_id INTEGER REFERENCES games(id),
   owner_id INTEGER NOT NULL REFERENCES users(id),
   opponent_id INTEGER REFERENCES users(id),
   current_player_id INTEGER REFERENCES users(id),
   step_count INTEGER DEFAULT 0,
   winner_id INTEGER REFERENCES users(id),
   field json,
   current_state STATE
);

CREATE OR REPLACE FUNCTION game_update_trigger()
    RETURNS TRIGGER
    LANGUAGE plpgsql
AS
$$
BEGIN
    INSERT INTO games_history(
        game_id,
        owner_id,
        opponent_id,
        current_player_id,
        step_count,
        winner_id,
        field,
        current_state
    )
    VALUES(
       NEW.id,
       NEW.owner_id,
       NEW.opponent_id,
       NEW.current_player_id,
       NEW.step_count,
       NEW.winner_id,
       NEW.field,
       NEW.current_state
    );
    RETURN NEW;
END;
$$;

CREATE OR REPLACE TRIGGER game_update
    AFTER UPDATE
    ON games
    FOR EACH ROW
EXECUTE PROCEDURE game_update_trigger();