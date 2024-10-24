import { defineStore } from 'pinia';
import apiClient from '../api/client';
import type { paths } from '@/types/schema'

type Message = paths['/inbox']['get']['responses']['200']['content']['application/json']['messages'][number]
type InboxResponse = paths['/inbox']['get']['responses']['200']['content']['application/json']

interface InboxState {
  messages: Message[];
  isLoading: boolean;
  error: string | null;
}

export const useInboxStore = defineStore('inbox', {
  state: (): InboxState => ({
    messages: [],
    isLoading: false,
    error: null,
  }),

  actions: {
    async fetchMessages() {
      this.isLoading = true;
      this.error = null;

      try {
        const { data, error } = await apiClient.GET('/inbox');

        if (error) {
          throw new Error('Failed to fetch messages');
        }

        if (data) {
          this.messages = (data as InboxResponse).messages;
        }
      } catch (err) {
        this.error = (err as Error).message;
      } finally {
        this.isLoading = false;
      }
    },

    // You can add more actions here, such as sending a message, marking as read, etc.
  },

  getters: {
    getMessages: (state): Message[] => state.messages,
    getIsLoading: (state): boolean => state.isLoading,
    getError: (state): string | null => state.error,
  },
});
