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
  return quizzes
}

/**
 * Load quizzes from API
 */
export async function loadQuizzes(): Promise<Quiz[]> {
  try {
    const response = await apiTransport.get<Quiz[]>('/quizzes')
    console.log('API response:', response)
    quizzes = response
    return quizzes
  } catch (error) {
    console.error('Failed to load quizzes:', error)
    if (error instanceof Error) {
      console.error('Error message:', error.message)
    }
    throw error // Re-throw the error to be caught in the component
  }
}
