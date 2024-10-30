<script setup lang="ts">
  import { onMounted, computed } from 'vue';
  import { Placeholder, Section, Sections } from '@/presentation/components';
  import { useInboxStore } from '@/store/inbox';

  const inboxStore = useInboxStore();

  const messages = computed(() => inboxStore.getMessages);
  const isLoading = computed(() => inboxStore.getIsLoading);
  const error = computed(() => inboxStore.getError);

  onMounted(async () => {
    await inboxStore.fetchMessages();
  });
</script>

<template>
  <div class="inbox-page">
    <div
      v-if="isLoading"
      class="loading"
    >
      Loading messages...
    </div>
    <div
      v-else-if="error"
      class="error"
    >
      {{ error }}
    </div>
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
        <div
          v-if="messages.length > 0"
          class="message-list"
        >
          <div
            v-for="message in messages"
            :key="message.created_at"
            class="message-item"
          >
            <div class="message-header">
              <p>{{ message.question.emoji }}</p>
            </div>
            <p>{{ message.question.text }}</p>
            <p>
              Taken by:
              {{ message.taker.first_name + ' ' + message.taker.last_name }}
            </p>
            <p>Date: {{ new Date(message.created_at).toLocaleString() }}</p>
          </div>
        </div>
        <div
          v-else
          class="no-messages"
        >
          No messages available.
        </div>
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

  .message-header {
    font-size: 24px;
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
