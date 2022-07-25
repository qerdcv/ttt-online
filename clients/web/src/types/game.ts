type Field = Array<Array<string>>;

export interface IGame {
  id: number,
  owner_id: number,
  step_count: number,

  field: Field,
  current_state: string,
  owner_mark: string,
  opponent_mark: string,

  opponent_id?: number,
  current_player_id?: number,
  winner_id: number,

}
