import { useCallback, useState } from 'react';
import axios, { AxiosResponse } from 'axios';

export interface IError {
  status?: number;
  message?: string;
}

interface IErrorResponse {
  message: string
}

export const useHttp = <T> () => {
	const [loading, setLoading] = useState<boolean>(false);
	const [error, setError] = useState<IError>({});

	const request = useCallback(async (callback: () => Promise<AxiosResponse<T>>): Promise<T> => {
		setLoading(true);
		setError({});

		try {
			const resp: AxiosResponse<T> = await callback();
			setLoading(false);
			return resp.data;
		} catch (e) {
			setLoading(false);
			if (axios.isAxiosError(e)) {
				setError({
					status: e.response?.status,
					message: (e.response?.data as IErrorResponse).message,
				});
			}

			throw e;
		}
	}, [setLoading, setError]);

	return { loading, error, request };
};
