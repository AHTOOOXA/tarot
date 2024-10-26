import { defineStore } from 'pinia';
import apiClient from '../api/client';
import type { paths } from '@/types/schema'

type InboxMessage = paths['/inbox']['get']['responses']['200']['content']['application/json']['messages'][number]

interface InboxState {
  messages: InboxMessage[];
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
          throw new Error('Failed to fetch inbox messages');
        }

        if (data) {
          this.messages = data.messages as InboxMessage[];
        }
      } catch (err) {
        this.error = (err as Error).message;
      } finally {
        this.isLoading = false;
      }
    },
  },

  getters: {
    getMessages: (state): InboxMessage[] => state.messages,
    getIsLoading: (state): boolean => state.isLoading,
    getError: (state): string | null => state.error,
  },
});
