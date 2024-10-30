import apiClient from '@/api/client';
import type { paths } from '@/types/schema';
import { StartParamKey } from '@/types/StartParamKey';

export function useInvite() {
  async function fetchInviteTokens(): Promise<
    paths['/invite_token']['get']['responses']['200']['content']['application/json']
  > {
    const { data, error } = await apiClient.GET('/invite_token');

    if (error) {
      throw new Error('Failed to fetch invite tokens');
    }

    if (data) {
      return data;
    }

    throw new Error('Invalid token data received');
  }

  async function constructInviteLink(): Promise<string> {
    const { user_token, group_token } = await fetchInviteTokens();
    const baseUrl = import.meta.env.VITE_BOT_URL;
    const startParam = `/app?startapp=${StartParamKey.FRIEND}-${user_token}-${StartParamKey.GROUP}-${group_token}`;
    return `${baseUrl}${startParam}`;
  }

  return {
    fetchInviteTokens,
    constructInviteLink,
  };
}
