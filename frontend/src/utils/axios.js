import axios from "axios"
import { API_BASE_URL } from "./constants"

/* 
apiInstance: to define default settings that will 
be applied to all requests made through apiInstance
*/
const apiInstance = axios.create({
    baseURL: API_BASE_URL,
    timeOut: 10000,
    headers: {
        "Content-Type": "application/json",
        Accept: "application/json"
    },
});

export default apiInstance