export type TField = Array<Array<Marks>>;
export type Coords = number[];

export enum GameState {
    pending = 'pending',
    inGame = 'in_game',
    done = 'done',
}

export enum Marks {
    noneMark = '',
    ownerMark = 'X',
    opponentMark = '0',
}

export interface IGame {
    id: number,
    owner_id: number,
    step_count: number,

    field: TField,
    current_state: GameState,
    owner_mark: string,
    opponent_mark: string,

    opponent_id?: number,
    current_player_id?: number,
    winner_id: number,
}

export const defaultGame: IGame = {
	current_state: GameState.pending,
	field: [
		[Marks.noneMark, Marks.noneMark, Marks.noneMark],
		[Marks.noneMark, Marks.noneMark, Marks.noneMark],
		[Marks.noneMark, Marks.noneMark, Marks.noneMark],
	],
	id: 0,
	opponent_mark: Marks.opponentMark,
	owner_id: 0,
	owner_mark: Marks.ownerMark,
	step_count: 0,
	winner_id: 0
};
