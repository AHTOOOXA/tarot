import { defineStore } from 'pinia';
import apiClient from '../api/client';
import type { paths } from '@/types/schema'

type User = paths['/user']['get']['responses']['200']['content']['application/json']
type UpdateUserRequest = paths['/user']['post']['requestBody']['content']['application/json']

interface UserState {
  user: User | null;
  friends: User[];
  error: string | null;
}

export const useUserStore = defineStore('user', {
  state: (): UserState => ({
    user: null,
    friends: [],
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

    async fetchFriends() {
      this.error = null;

      try {
        const { data, error } = await apiClient.GET('/friends');

        if (error) {
          throw new Error('Failed to fetch friends');
        }

        if (data) {
          this.friends = data as User[];
        }
      } catch (err) {
        this.error = (err as Error).message;
      }
    },

    async fetchUserById(userId: number) {
      this.error = null;
      const { data, error } = await apiClient.GET('/user/{user_id}', {
        params: {
          path: { user_id: userId },
        },
      });

      if (error) {
        throw new Error('Failed to fetch user');
      }

      return data as User;
    },

    async addFriend(friendId: number) {
      this.error = null;

      if (!Number.isNaN(friendId) && Number.isFinite(friendId)) {
        try {
          const { data, error } = await apiClient.POST('/add_friend', {
            params: { query: { friend_id: friendId } },
          });

          if (error) {
            throw new Error('Failed to add friend');
          }

          // Handle successful friend addition here
          // For example, you might want to update the friends list
          // await this.fetchFriends();

        } catch (err) {
          this.error = (err as Error).message;
        }
      } else {
        this.error = 'Invalid friend ID';
      }
    },
  },

  getters: {
    getUser: (state): User | null => state.user,
    getFriends: (state): User[] => state.friends,
    getError: (state): string | null => state.error,
  },
});
