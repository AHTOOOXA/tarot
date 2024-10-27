import { ref } from 'vue'
import useTelegram from '@/services/useTelegram'
import apiClient from '@/api/client'
import type { paths } from '@/types/schema'

// Define available parameters
export enum StartParamKey {
  FRIEND = 'f',
  GROUP = 'g',
  // Add more parameter keys as needed
}

type StartParams = Partial<Record<StartParamKey, string>>;

const startParams = ref<StartParams>({})

export function useStart() {
  const { webAppInitData } = useTelegram()

  function parseStartParam() {
    const initData = new URLSearchParams(webAppInitData)
    const startParamString = initData.get('start_param')
    if (startParamString) {
      const params = startParamString.split('-')
      for (let i = 0; i < params.length; i += 2) {
        if (i + 1 < params.length) {
          const key = Object.entries(StartParamKey).find(([_, value]) => value === params[i])?.[0]
          if (key) {
            startParams.value[StartParamKey[key as keyof typeof StartParamKey]] = params[i + 1]
          }
        }
      }
    }
  }

  function getStartParam(key: StartParamKey): string | undefined {
    return startParams.value[key]
  }

  function getAllStartParams(): StartParams {
    return startParams.value
  }

  async function fetchInviteTokens(): Promise<paths['/invite_token']['get']['responses']['200']['content']['application/json']> {
    const { data, error } = await apiClient.GET('/invite_token')

    if (error) {
      throw new Error('Failed to fetch invite tokens');
    }

    if (data) {
      return data;
    }

    throw new Error('Invalid token data received');
  }

  async function constructInviteLink(): Promise<string> {
    const { user_token, group_token } = await fetchInviteTokens()
    const baseUrl = import.meta.env.VITE_BOT_URL
    console.log(baseUrl)
    const startParam = `/startapp?${StartParamKey.FRIEND}=${user_token}&${StartParamKey.GROUP}=${group_token}`
    return `${baseUrl}${startParam}`
  }

  return {
    parseStartParam,
    getStartParam,
    getAllStartParams,
    constructInviteLink,
    StartParamKey,
  }
}
