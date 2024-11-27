import { defineStore } from 'pinia';
import apiClient from '@/api/client';
import type { components } from '@/types/schema';

type TarotCard = components['schemas']['TarotCard-Output'];

interface TarotState {
  cards: TarotCard[];
  error: string | null;
}

export const useTarotStore = defineStore('tarot', {
  state: (): TarotState => ({
    cards: [],
    error: null,
  }),

  actions: {
    async fetchDailyCards() {
      this.error = null;

      const { data, error } = await apiClient.GET('/tarot/draw_daily_card');

      if (error) {
        this.error = 'Failed to fetch cards';
        console.error('Failed to fetch cards:', error);
      } else if (data) {
        this.cards = data;
      }
    },

    async selectDailyCard(card: TarotCard) {
      this.error = null;

      const { error } = await apiClient.POST('/tarot/select_daily_card', {
        body: {
          id: card.id,
          key: card.key,
        },
      });

      if (error) {
        this.error = 'Failed to select card';
        console.error('Failed to select card:', error);
      }
    },
  },
});
