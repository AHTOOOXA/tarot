import type UserProfile from '@/domain/entities/UserProfile'
import { apiTransport } from '@/infra/transport/api'

/**
 * Profile Store
 * ---------------------------
 */

let profile: UserProfile | null = null

/**
 * Get user profile
 */
export function getProfile(): UserProfile | null {
  return profile
}

/**
 * Load user profile from API
 */
export async function loadProfile(): Promise<UserProfile> {
  try {
    const response = await apiTransport.get<UserProfile>('/profile')
    console.log('API response:', response)
    profile = response
    return profile
  } catch (error) {
    console.error('Failed to load profile:', error)
    if (error instanceof Error) {
      console.error('Error message:', error.message)
    }
    throw error // Re-throw the error to be caught in the component
  }
}
