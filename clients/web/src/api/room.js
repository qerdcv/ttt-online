import { Api } from "api";



export const Room = {
  create: (params) => Api.post("/api/room", params),
  get: (params) => Api.get("/api/room", params),
  getOne: (_id, params) => Api.get(`/api/room/${_id}`, params)
}
