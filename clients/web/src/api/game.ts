import { Api } from 'api/index';
import { IGame, Coords } from 'types/game';

interface IGameStepRequest {
    coords: Coords
}

export const Game = {
    async create() {
        return await Api.post('/api/games');
    },

    async getByID(gameID?: string): Promise<IGame> {
        return await Api.get(`/api/games/${gameID}`);
    },

    async loginGame(gameID?: number) {
        return await Api.patch(`/api/games/${gameID}/login`);
    },

    async step(req: IGameStepRequest, gameID: number): Promise<IGame> {
        return await Api.patch(`/api/games/${gameID}`, req);
    }
};
