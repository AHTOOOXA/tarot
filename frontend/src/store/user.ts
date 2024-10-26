import { defineStore } from 'pinia';
import apiClient from '../api/client';
import type { paths } from '@/types/schema'

type User = paths['/user']['get']['responses']['200']['content']['application/json']
type UpdateUserRequest = paths['/user']['post']['requestBody']['content']['application/json']

interface UserState {
  user: User | null;
  error: string | null;
}

export const useUserStore = defineStore('user', {
  state: (): UserState => ({
    user: null,
    error: null,
  }),

  actions: {
    async fetchUser() {
      this.error = null;

      try {
        const { data, error } = await apiClient.GET('/user');

        if (error) {
          throw new Error('Failed to fetch user');
        }

        if (data) {
          this.user = data as User;
        }
      } catch (err) {
        this.error = (err as Error).message;
      }
    },

    async updateUser(updatedUser: UpdateUserRequest) {
      this.error = null;

      try {
        const { data, error } = await apiClient.POST('/user', {
          body: updatedUser,
        });

        if (error) {
          throw new Error('Failed to update user');
        }

        if (data) {
          this.user = data as User;
        }
      } catch (err) {
        this.error = (err as Error).message;
      }
    },
  },

  getters: {
    getUser: (state): User | null => state.user,
    getError: (state): string | null => state.error,
  },
});
