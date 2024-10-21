import { ref, type Ref } from 'vue'
import type Quiz from '../entities/Quiz'
import { createSharedComposable } from '@vueuse/core'
import { getQuizzes, loadQuizzes, submitQuizResponse as submitQuizResponseToStore } from '@/infra/store/quizzes'

interface UseQuizzesComposableState {
  /**
   * Quizzes
   */
  quizzes: Ref<Quiz[]>;
  /**
   * Load quizzes
   */
  load: () => Promise<void>;
  /**
   * Submit quiz response
   */
  submitQuizResponse: (response: { question_id: number; answer_id: number }) => Promise<void>;
}

/**
 * Composable to work with quizzes
 */
export const useQuizzes = createSharedComposable((): UseQuizzesComposableState => {
  const quizzes = ref<Quiz[]>(getQuizzes())

  const load = async () => {
    quizzes.value = await loadQuizzes()
  }

  const submitQuizResponse = async (response: { question_id: number; answer_id: number }) => {
    await submitQuizResponseToStore(response)
  }

  return {
    quizzes,
    load,
    submitQuizResponse,
  }
})
