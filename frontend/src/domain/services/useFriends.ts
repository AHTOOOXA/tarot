import { ref, type Ref } from 'vue'
import type User from '../entities/User'
import { createSharedComposable } from '@vueuse/core'
import { getFriends, loadFriends, addFriend } from '@/infra/store/friends'

interface useFriendsComposableState {
  /**
   * Friends list
   */
  friends: Ref<User[]>;
  /**
   * Load friends
   */
  load: () => Promise<void>;
  /**
   * Add a new friend
   */
  add: (friendId: number) => Promise<boolean>;
}

/**
 * Composable to work with friends list
 */
export const useFriends = createSharedComposable((): useFriendsComposableState => {
  const friends = ref<User[]>(getFriends())

  const load = async () => {
    const loadedFriends = await loadFriends()
    friends.value = loadedFriends
    console.log('Friends loaded in composable:', friends.value)
  }

  const add = async (friendId: number) => {
    const success = await addFriend(friendId)
    if (success) {
      await load() // Reload friends list after successful addition
    }
    return success
  }

  return {
    friends,
    load,
    add,
  }
})
