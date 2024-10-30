import { ref } from 'vue';
import useTelegram from '@/services/useTelegram';
import apiClient from '@/api/client';
import { useUserStore } from '@/store/user';
import { useInviterStore } from '@/store/inviter';
import type { components } from '@/types/schema';
import { StartParamKey } from '@/types/StartParamKey';

type StartParams = Partial<Record<StartParamKey, string>>;
type StartData = components['schemas']['StartData'];

const startParams = ref<StartParams>({});

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
    const userStore = useUserStore();
    const inviterStore = useInviterStore();

    userStore.setUser(data.current_user);
    inviterStore.setInviter(data.inviter);
  }
}

export function useStart() {
  return {
    StartParamKey,
  };
}
