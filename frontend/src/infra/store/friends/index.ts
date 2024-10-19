import type User from '@/domain/entities/User'
import { apiTransport } from '@/infra/transport/api'

/**
 * Friends Store
 * ---------------------------
 */

let friends: User[] = []

/**
 * Get friends list
 */
export function getFriends(): User[] {
  return friends
}

/**
 * Load friends from API
 */
export async function loadFriends(): Promise<User[]> {
  try {
    const response = await apiTransport.get<User[]>('/friends')
    console.log('API response:', response)
    friends = response
    return friends
  } catch (error) {
    console.error('Failed to load friends:', error)
    if (error instanceof Error) {
      console.error('Error message:', error.message)
    }
    throw error // Re-throw the error to be caught in the component
  }
}

/**
 * Add a new friend
 * @param friendId - The user ID of the friend to add
 */
export async function addFriend(friendId: number): Promise<boolean> {
  try {
    const response = await apiTransport.post<{ success: boolean }>('/add_friend', { friend_id: friendId })
    console.log('Add friend API response:', response)

    if (response.success) {
      // Reload friends list to get the updated list including the new friend
      await loadFriends()
    }

    return response.success
  } catch (error) {
    console.error('Failed to add friend:', error)
    if (error instanceof Error) {
      console.error('Error message:', error.message)
    }
    throw error // Re-throw the error to be caught in the component
  }
}
