import { Api } from 'api/index';
import { IGame, Coords } from 'types/game';
import { AxiosResponse } from 'axios';

interface IGameStepRequest {
    coords: Coords
}

export const Game = {
  async create(): Promise<AxiosResponse<IGame>> {
    return await Api.post<IGame>('/api/games');
  },

  async getByID(gameID = ''): Promise<AxiosResponse<IGame>> {
    return await Api.get<IGame>(`/api/games/${gameID}`);
  },

  async loginGame(gameID: number): Promise<AxiosResponse<IGame>> {
    return await Api.patch<IGame>(`/api/games/${gameID}/login`);
  },

  async step(req: IGameStepRequest, gameID: number): Promise<AxiosResponse<IGame>> {
    return await Api.patch<IGame>(`/api/games/${gameID}`, req);
  }
};
