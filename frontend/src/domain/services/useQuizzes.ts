import { ref, type Ref } from 'vue'
import type Quiz from '../entities/Quiz'
import { createSharedComposable } from '@vueuse/core'
import { getQuizzes, loadQuizzes } from '@/infra/store/quizzes'

interface useQuizzesComposableState {
  /**
   * Quizzes
   */
  quizzes: Ref<Quiz[]>;
  /**
   * Load quizzes
   */
  load: () => Promise<void>;
}

/**
 * Composable to work with quizzes
 */
export const useQuizzes = createSharedComposable((): useQuizzesComposableState => {
  const quizzes = ref<Quiz[]>(getQuizzes())

  const load = async () => {
    const loadedQuizzes = await loadQuizzes()
    quizzes.value = loadedQuizzes
    console.log('Quizzes loaded in composable:', quizzes.value)
  }

  return {
    quizzes,
    load,
  }
})
