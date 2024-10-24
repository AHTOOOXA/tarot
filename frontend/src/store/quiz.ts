import { defineStore } from 'pinia';
import apiClient from '../api/client';
import type { paths } from '@/types/schema'

type Quiz = paths['/quizzes']['get']['responses']['200']['content']['application/json']['quizzes'][number]
type QuizList = paths['/quizzes']['get']['responses']['200']['content']['application/json']
type QuizResponse = paths['/quiz_response']['post']['requestBody']['content']['application/json']

interface QuizState {
  quizzes: Quiz[];
  isLoading: boolean;
  error: string | null;
}

export const useQuizStore = defineStore('quiz', {
  state: (): QuizState => ({
    quizzes: [],
    isLoading: false,
    error: null,
  }),

  actions: {
    async fetchQuizzes() {
      this.isLoading = true;
      this.error = null;

      try {
        const { data, error } = await apiClient.GET('/quizzes');

        if (error) {
          throw new Error('Failed to fetch quizzes');
        }

        if (data) {
          this.quizzes = (data as QuizList).quizzes;
        }
      } catch (err) {
        this.error = (err as Error).message;
      } finally {
        this.isLoading = false;
      }
    },

    async submitQuizResponse(takerId: number, questionId: number, answerId: number) {
      this.error = null;

      try {
        const requestBody: QuizResponse = {
          taker_id: takerId,
          question_id: questionId,
          answer_id: answerId,
        };

        const { error } = await apiClient.POST('/quiz_response', {
          body: requestBody,
        });

        if (error) {
          throw new Error('Failed to submit quiz response');
        }
      } catch (err) {
        this.error = (err as Error).message;
      }
    },
  },

  getters: {
    getQuizzes: (state): Quiz[] => state.quizzes,
    getIsLoading: (state): boolean => state.isLoading,
    getError: (state): string | null => state.error,
  },
});
