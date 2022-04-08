import { useState } from 'react';
import axios, { AxiosError } from 'axios';

export interface IError {
  status?: number;
  message?: string;
}

export const useHttp = () => {
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<IError>({});

  const request = async (callback: any, params?: object) => {
    let data = null;
    setLoading(true);
    setError({});

    try {
      data = (await callback(JSON.stringify(params))).data;
      setLoading(false);
    } catch (e) {
      setLoading(false);
      if (axios.isAxiosError(e)) {
        let aErr = e as AxiosError;
        setError({
          status: aErr.response?.status,
          message: aErr.response?.data['message'],
        });
      } else {
        throw e;
      }
    }
    return data;
  };

  return { loading, error, request };
};
