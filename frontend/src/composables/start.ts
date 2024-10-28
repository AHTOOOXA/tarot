import { ref } from 'vue';
import useTelegram from '@/services/useTelegram';
import apiClient from '@/api/client';
import type { paths } from '@/types/schema';
import type { components } from '@/types/schema';

// Define available parameters
export enum StartParamKey {
  FRIEND = 'f',
  GROUP = 'g',
  REFERAL = 'r',
}

type StartParams = Partial<Record<StartParamKey, string>>;
type StartData = components['schemas']['StartData'];

const startParams = ref<StartParams>({});
const startData = ref<StartData | null>(null);

// Parse start parameters on initialization
const { webAppInitData } = useTelegram();
const initData = new URLSearchParams(webAppInitData);
const startParamString = initData.get('start_param');
if (startParamString) {
  const params = startParamString.split('-');
  for (let i = 0; i < params.length; i += 2) {
    if (i + 1 < params.length) {
      const key = Object.entries(StartParamKey).find(([_, value]) => value === params[i])?.[0];
      if (key) {
        startParams.value[StartParamKey[key as keyof typeof StartParamKey]] = params[i + 1];
      }
    }
  }
}

export async function processStart(): Promise<void> {
  const userToken = startParams.value[StartParamKey.FRIEND];
  const groupToken = startParams.value[StartParamKey.GROUP];
  const referalId = startParams.value[StartParamKey.REFERAL];

  const { data, error } = await apiClient.POST('/process_start', {
    body: {
      user_token: userToken || '',
      group_token: groupToken || '',
      referal_id: referalId || '',
    },
  });

  if (error) {
    throw new Error('Failed to process start parameters');
  }

  if (data) {
    startData.value = data;
  }
}

export function useStart() {
  function getStartData(): StartData | null {
    return startData.value;
  }

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
    getStartData,
    constructInviteLink,
    StartParamKey,
  };
}
