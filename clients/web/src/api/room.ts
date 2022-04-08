import { Api } from 'api';

export const Room = {
  create: () => Api.post('/api/games'),
  get: () => Api.get('/api/games'),
  getOne: (id: string) => Api.get(`/api/room/${id}`),
};
