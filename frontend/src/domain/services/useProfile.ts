import { ref, type Ref } from 'vue'
import type UserProfile from '../entities/UserProfile'
import { createSharedComposable } from '@vueuse/core'
import { getProfile, loadProfile } from '@/infra/store/profile'

interface useProfileComposableState {
  /**
   * User Profile
   */
  profile: Ref<UserProfile | null>;
  /**
   * Load user profile
   */
  load: () => Promise<void>;
}

/**
 * Composable to work with user profile
 */
export const useProfile = createSharedComposable((): useProfileComposableState => {
  const profile = ref<UserProfile | null>(getProfile())

  const load = async () => {
    const loadedProfile = await loadProfile()
    profile.value = loadedProfile
    console.log('Profile loaded in composable:', profile.value)
  }

  return {
    profile,
    load,
  }
})
