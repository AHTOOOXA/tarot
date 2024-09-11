import type Question from '@/domain/entities/Question.js'
import { apiTransport } from '@/infra/transport/api'

/**
 * Questions Store
 * ---------------------------
 */

let questions: Question[] = []

/**
 * Get all questions
 */
export function getQuestions(): Question[] {
  return questions
}

/**
 * Get question by id
 *
 * @param id - Question id
 */
export function getQuestionById(id: Question['question_id']): Question | undefined {
  return questions.find((q) => q.question_id === id)
}

/**
 * Load questions from API
 */
export async function loadQuestions(): Promise<Question[]> {
  try {
    const response = await apiTransport.get<Question[]>('/questions')
    console.log('API response:', response)
    questions = response
    return questions
  } catch (error) {
    console.error('Failed to load questions:', error)
    if (error instanceof Error) {
      console.error('Error message:', error.message)
    }
    throw error // Re-throw the error to be caught in the component
  }
}