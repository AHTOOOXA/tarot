import type Message from '@/domain/entities/Message'
import { apiTransport } from '@/infra/transport/api'

/**
 * Inbox Store
 * ---------------------------
 */

let messages: Message[] = []

/**
 * Get all messages
 */
export function getMessages(): Message[] {
  return [...messages]
}

/**
 * Load messages from API
 */
export async function loadMessages(): Promise<Message[]> {
  try {
    const response = await apiTransport.get<{ messages: Message[] }>('/inbox')
    if (Array.isArray(response.messages)) {
      messages = response.messages
    } else {
      console.error('Unexpected response format:', response)
      messages = []
    }
    return [...messages]
  } catch (error) {
    console.error('Failed to load messages:', error)
    messages = []
    throw error
  }
}
