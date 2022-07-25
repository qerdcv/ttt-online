import { Api } from 'api/index';

export const Game = {
    async create() {
       return await Api.post('/api/games')
    }
};
