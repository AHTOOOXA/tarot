import { ref, type Ref } from 'vue'
import type Question from '../entities/Question'
import { createSharedComposable } from '@vueuse/core'
import { getQuestions, loadQuestions } from '@/infra/store/questions'

interface useQuestionsComposableState {
  /**
   * Questions
   */
  questions: Ref<Question[]>;
  /**
   * Load questions
   */
  load: () => Promise<void>;
}

/**
 * Composable to work with questions
 */
export const useQuestions = createSharedComposable((): useQuestionsComposableState => {
  const questions = ref<Question[]>(getQuestions())

  const load = async () => {
    const loadedQuestions = await loadQuestions()
    questions.value = loadedQuestions
    console.log('Questions loaded in composable:', questions.value)
  }

  return {
    questions,
    load,
  }
})