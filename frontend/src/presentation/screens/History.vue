<script setup lang="ts">
import { Placeholder, Section, Sections } from '@/presentation/components';
</script>

<template>
  <div class="history-page">
    <Sections>
      <Section standalone>
        <Placeholder
          title="Coming Soon"
          caption="History feature is under development"
          standalone
        >
          <template #picture>
            <div class="history-icon">📜</div>
          </template>
        </Placeholder>
      </Section>
      <Section padded>
        <div class="history-content">
          <div class="coming-soon-message">Your story will be written here soon!</div>
        </div>
      </Section>
    </Sections>
  </div>
</template>

<style scoped>
.history-page {
  display: flex;
  flex-direction: column;
  min-height: 100%;
}

.history-icon {
  font-size: 48px;
  width: var(--size-avatar-big);
  height: var(--size-avatar-big);
  display: flex;
  align-items: center;
  justify-content: center;
}

.history-content {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-10);
}

.coming-soon-message {
  padding: var(--spacing-10);
  background-color: var(--color-bg-tertiary);
  border-radius: var(--size-border-radius-medium);
  text-align: center;
}
</style>
