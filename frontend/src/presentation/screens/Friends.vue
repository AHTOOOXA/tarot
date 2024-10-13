<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Placeholder, Section, Sections } from '@/presentation/components'
import useTelegram from '@/application/services/useTelegram'

const { webAppInitData } = useTelegram()
const isLoading = ref(true)
const error = ref<string | null>(null)
const friends = ref<any[]>([])

const currentUserId = ref('')

onMounted(async () => {
  try {
    isLoading.value = true
    // Parse webAppInitData to get user information
    const initData = new URLSearchParams(webAppInitData)
    const user = JSON.parse(initData.get('user') || '{}')
    currentUserId.value = user.id?.toString() || ''

    // Simulating API call to get friends
    await new Promise(resolve => setTimeout(resolve, 1000))
    friends.value = [
      { id: 1, name: 'Alice Johnson', status: 'online' },
      { id: 2, name: 'Bob Williams', status: 'offline' },
    ]
  } catch (e) {
    error.value = 'Failed to load friends. Please try again later.'
    console.error('Error loading friends:', e)
  } finally {
    isLoading.value = false
  }
})

const inviteFriends = () => {
  const baseUrl = 'https://t.me/anton_local_dev_bot/start'
  const friendParam = `friend=${currentUserId.value}`
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
          <div v-if="friends.length > 0" class="friends-content">
            <div class="invite-friends-button" @click="inviteFriends">
              Invite Friends
            </div>
            <div v-for="friend in friends" :key="friend.id" class="friend-item">
              <h3>{{ friend.name }}</h3>
              <p>Status: {{ friend.status }}</p>
            </div>
          </div>
          <div v-else class="no-friends">No friends available.</div>
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
}

.friend-item {
  padding: var(--spacing-10);
  background-color: var(--color-bg-tertiary);
  border-radius: var(--size-border-radius-medium);
}

.friend-item h3 {
  margin: 0 0 var(--spacing-5) 0;
}

.friend-item p {
  margin: 0;
}
</style>
