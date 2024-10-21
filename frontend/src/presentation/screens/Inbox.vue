<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Placeholder, Section, Sections } from '@/presentation/components'
import { useInbox } from '@/domain/services/useInbox'

const { messages, load } = useInbox()
const isLoading = ref(true)
const error = ref<string | null>(null)

onMounted(async () => {
  try {
    isLoading.value = true
    await load()
    console.log('Loaded messages:', messages.value)
  } catch (e) {
    error.value = 'Failed to load messages. Please try again later.'
    console.error('Error loading messages:', e)
  } finally {
    isLoading.value = false
  }
})
</script>

<template>
  <div class="inbox-page">
    <div v-if="isLoading" class="loading">Loading messages...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <Sections v-else>
      <Section standalone>
        <Placeholder
          title="Inbox"
          caption="Your messages"
          standalone
        >
          <template #picture>
            <div class="inbox-icon">📥</div>
          </template>
        </Placeholder>
      </Section>
      <Section padded>
        <div v-if="messages.length > 0" class="message-list">
          <div v-for="message in messages" :key="message.created_at" class="message-item">
            <h3>{{ message.question.text }}</h3>
            <p>Taken by: {{ message.taker.first_name + ' ' + message.taker.last_name }}</p>
            <p>Date: {{ new Date(message.created_at).toLocaleString() }}</p>
          </div>
        </div>
        <div v-else class="no-messages">No messages available.</div>
      </Section>
    </Sections>
  </div>
</template>

<style scoped>
.inbox-page {
  display: flex;
  flex-direction: column;
  min-height: 100%;
}

.inbox-icon {
  font-size: 48px;
  width: var(--size-avatar-big);
  height: var(--size-avatar-big);
  display: flex;
  align-items: center;
  justify-content: center;
}

.message-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-10);
}

.message-item {
  padding: var(--spacing-10);
  background-color: var(--color-bg-tertiary);
  border-radius: var(--size-border-radius-medium);
}

.message-item h3 {
  margin: 0 0 var(--spacing-5) 0;
}

.message-item p {
  margin: 0;
}
</style>
