<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Placeholder, Section, Sections } from '@/presentation/components'

const isLoading = ref(true)
const error = ref<string | null>(null)
const friends = ref<any[]>([])

onMounted(async () => {
  try {
    isLoading.value = true
    // Simulating API call
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
        <div v-if="friends.length > 0" class="friend-list">
          <div v-for="friend in friends" :key="friend.id" class="friend-item">
            <h3>{{ friend.name }}</h3>
            <p>Status: {{ friend.status }}</p>
          </div>
        </div>
        <div v-else class="no-friends">No friends available.</div>
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

.friend-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-10);
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
