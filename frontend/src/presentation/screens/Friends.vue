<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { Placeholder, Section, Sections } from '@/presentation/components'
import { useUserStore } from '@/store/user'
import type { paths } from '@/types/schema'

type User = paths['/user']['get']['responses']['200']['content']['application/json']

const userStore = useUserStore()
const isLoading = ref(true)
const error = ref<string | null>(null)

const user = computed(() => userStore.getUser)
const friends = computed(() => userStore.getFriends)

onMounted(async () => {
  try {
    isLoading.value = true
    await Promise.all([
      userStore.fetchUser(),
      userStore.fetchFriends()
    ])
  } catch (e) {
    error.value = 'Failed to load friends. Please try again later.'
    console.error('Error loading friends:', e)
  } finally {
    isLoading.value = false
  }
})

const inviteFriends = () => {
  if (!user.value) return

  const baseUrl = 'https://t.me/anton_local_dev_bot/app'
  const friendParam = `startapp=${user.value.user_id}`
  const textParam = encodeURIComponent('Добавь меня в друзья в Glow App')
  const shareUrl = `https://t.me/share/url?url=${encodeURIComponent(`${baseUrl}?${friendParam}`)}&text=${textParam}`
  window.open(shareUrl, '_blank')
}
</script>

<template>
  <div class="friends-page">
    <div v-if="isLoading" class="loading">Loading friends...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <Sections v-else>
      <Section standalone>
        <Placeholder
          title="Friends"
          caption="Your friend list"
          standalone
        >
          <template #picture>
            <div class="friends-icon">👥</div>
          </template>
        </Placeholder>
      </Section>
      <Section padded>
        <div>
          <div class="friends-content">
            <div class="invite-friends-button" @click="inviteFriends">
              Invite Friends
            </div>
            <div v-if="friends.length > 0">
              <div v-for="friend in friends" :key="friend.user_id" class="friend-item">
                <h3>{{ friend.first_name }} {{ friend.last_name }}</h3>
                <img v-if="friend.photo_url" :src="friend.photo_url" alt="Friend's photo" class="friend-photo">
              </div>
            </div>
            <div v-else class="no-friends">No friends available.</div>
          </div>
        </div>
      </Section>
    </Sections>
  </div>
</template>

<style scoped>
.friends-page {
  display: flex;
  flex-direction: column;
  min-height: 100%;
}

.friends-icon {
  font-size: 48px;
  width: var(--size-avatar-big);
  height: var(--size-avatar-big);
  display: flex;
  align-items: center;
  justify-content: center;
}

.friends-content {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-10);
}

.invite-friends-button {
  padding: var(--spacing-10);
  background-color: #4CAF50; /* Green color */
  border-radius: var(--size-border-radius-medium);
  color: white;
  text-align: center;
  font-weight: bold;
  transition: background-color 0.3s ease;
  cursor: pointer;
}

.friend-item {
  padding: var(--spacing-10);
  background-color: var(--color-bg-tertiary);
  border-radius: var(--size-border-radius-medium);
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.friend-item h3 {
  margin: 0 0 var(--spacing-5) 0;
}

.friend-item p {
  margin: 0;
}

.friend-photo {
  width: var(--size-avatar-medium);
  height: var(--size-avatar-medium);
  border-radius: 50%;
  object-fit: cover;
  margin-top: var(--spacing-5);
}
</style>
