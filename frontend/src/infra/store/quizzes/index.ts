import type Quiz from '@/domain/entities/Quiz.js'
import { apiTransport } from '@/infra/transport/api'

/**
 * Quizzes Store
 * ---------------------------
 */

let quizzes: Quiz[] = []

/**
 * Get all quizzes
 */
export function getQuizzes(): Quiz[] {
  return [...quizzes]
}

/**
 * Load quizzes from API
 */
export async function loadQuizzes(): Promise<Quiz[]> {
  try {
    const response = await apiTransport.get<{ quizzes: Quiz[] }>('/quizzes')
    if (Array.isArray(response.quizzes)) {
      quizzes = response.quizzes
    } else {
      console.error('Unexpected response format:', response)
      quizzes = []
    }
    return [...quizzes]
  } catch (error) {
    console.error('Failed to load quizzes:', error)
    quizzes = []
    throw error
  }
}

/**
 * Submit a quiz response
 */
export async function submitQuizResponse(response: { question_id: number; answer_id: number }): Promise<void> {
  try {
    await apiTransport.post('/quiz_response', response)
  } catch (error) {
    console.error('Failed to submit quiz response:', error)
    throw error
  }
}
