import { defineStore } from 'pinia';
import type { components } from '@/types/schema';

type Inviter = components['schemas']['StartData']['inviter'];

interface InviterState {
  inviter: Inviter | null;
}

export const useInviterStore = defineStore('inviter', {
  state: (): InviterState => ({
    inviter: null,
  }),

  actions: {
    setInviter(inviter: Inviter | null) {
      this.inviter = inviter;
    },

    processInvite() {
      this.inviter = null;
    },
  },

  getters: {
    getInviter: (state): Inviter | null => state.inviter,
  },
});
