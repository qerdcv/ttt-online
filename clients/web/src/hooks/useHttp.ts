import { useCallback, useState } from 'react';
import axios, { AxiosError } from 'axios';

export interface IError {
  status?: number;
  message?: string;
}

export const useHttp = <T> () => {
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<IError>({});

  const request = useCallback(async <V> (callback: any, params?: V): Promise<T> => {
    let data: T;
    setLoading(true);
    setError({});

    try {
      const resp = await callback();
      data = resp.data;
      setLoading(false);
    } catch (e) {
      setLoading(false);
      if (axios.isAxiosError(e)) {
        let aErr = e as AxiosError;
        setError({
          status: aErr.response?.status,
          message: aErr.response?.data['message'],
        });
      }

      throw e;
    }
    return data;
  }, [setLoading, setError]);

  return { loading, error, request };
};
