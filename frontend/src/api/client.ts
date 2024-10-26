import createClient from "openapi-fetch";
import type { paths } from '../types/schema';

const API_HOST = import.meta.env.VITE_API_HOST || 'http://localhost:3779'
const apiClient = createClient<paths>({
  baseUrl: API_HOST,
});

export default apiClient;
