import { Api } from 'api';


export interface IUserRequest {
    username: string
    password: string
}

export const Auth = {
	async login(user: IUserRequest) {
		return await Api.post('/api/login', user);
	},

	async register(user: IUserRequest) {
		return await Api.post('/api/registration', user);
	},

	async logout() {
		return await Api.get('/api/logout');
	},
};
