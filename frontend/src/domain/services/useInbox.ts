import { ref, type Ref } from 'vue'
import type Message from '../entities/Message'
import { createSharedComposable } from '@vueuse/core'
import { getMessages, loadMessages } from '@/infra/store/inbox'

interface UseInboxComposableState {
  /**
   * Messages
   */
  messages: Ref<Message[]>;
  /**
   * Load messages
   */
  load: () => Promise<void>;
}

/**
 * Composable to work with inbox messages
 */
export const useInbox = createSharedComposable((): UseInboxComposableState => {
  const messages = ref<Message[]>(getMessages())

  const load = async () => {
    messages.value = await loadMessages()
  }

  return {
    messages,
    load,
  }
})
