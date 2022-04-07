import { useState } from "react";

export const useHttp = () => {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState({})

  const request = async (callback, params) => {
    let data = null;
    setLoading(true)
    setError({})

    try {
      data = (await callback(JSON.stringify(params))).data
      setLoading(false)
    } catch (e) {
      setLoading(false)
      setError({
        status: e.status,
        message: e.message,
      })
    }
    return data
  }

  return {loading, error, request}
}