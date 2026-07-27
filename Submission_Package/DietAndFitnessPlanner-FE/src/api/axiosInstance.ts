import axios from "axios";

const apiBaseURL = import.meta.env.VITE_API_BASE_URL?.trim() || (import.meta.env.DEV ? "http://127.0.0.1:8001" : "");

export default axios.create({
  baseURL: apiBaseURL,
});

