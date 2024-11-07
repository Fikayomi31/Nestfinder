import UserData from "../views/plugin/UserData";

export const API_BASE_URL = `http://127.0.0.1:8000/api/v1`
export const tenantId = UserData()?.tenantId
export const agentId = UserData()?.agentId