import { ref } from 'vue'
import useTelegram from '@/services/useTelegram'

interface StartParams {
  [key: string]: string;
}

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
          startParams.value[params[i]] = params[i + 1]
        }
      }
    }
  }

  function getStartParam(key: string): string | undefined {
    return startParams.value[key]
  }

  function getAllStartParams(): StartParams {
    return startParams.value
  }

  return {
    parseStartParam,
    getStartParam,
    getAllStartParams,
  }
}
