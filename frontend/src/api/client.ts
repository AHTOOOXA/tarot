import createClient from "openapi-fetch";
import type { paths } from '../types/schema';
import useTelegram from '@/services/useTelegram';

const { webAppInitData } = useTelegram();

const API_HOST = import.meta.env.VITE_API_HOST || 'http://localhost:3779'
const apiClient = createClient<paths>({
  baseUrl: API_HOST,
  headers: {
    'initData': webAppInitData,
  },
});

export default apiClient;
