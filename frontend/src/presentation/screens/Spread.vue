<script setup lang="ts">
import { Placeholder, Section, Sections, List, ListItem } from '@/presentation/components';

const spreads = [
  {
    title: 'Daily Spread',
    icon: '🌅',
    description: 'Get insights for your day',
    isComingSoon: false,
    route: 'daily-spread',
  },
  {
    title: 'Ask a Question',
    icon: '❓',
    description: 'Get answers to your specific questions',
    isComingSoon: true,
    route: 'ask-question',
  },
  {
    title: 'Love Spread',
    icon: '❤️',
    description: 'Insights about your relationships',
    isComingSoon: true,
    route: 'love-spread',
  },
];
</script>

<template>
  <div class="spread-page">
    <Sections>
      <Section standalone>
        <Placeholder
          title="Spreads"
          caption="Choose your reading"
          standalone
        >
          <template #picture>
            <div class="spread-icon">🔮</div>
          </template>
        </Placeholder>
      </Section>
      <Section padded>
        <List
          standalone
          gapped
        >
          <ListItem
            v-for="spread in spreads"
            :key="spread.title"
            :title="spread.title"
            :subtitle="spread.description"
            :icon="spread.icon"
            :is-emoji="true"
            :class="{ disabled: spread.isComingSoon }"
            right-icon="arrow-right-fill"
            standalone
          >
            <template
              v-if="spread.isComingSoon"
              #right
            >
              <span class="coming-soon-badge">Coming Soon</span>
            </template>
          </ListItem>
        </List>
      </Section>
    </Sections>
  </div>
</template>

<style scoped>
.spread-page {
  display: flex;
  flex-direction: column;
  min-height: 100%;
}

.spread-icon {
  font-size: 48px;
  width: var(--size-avatar-big);
  height: var(--size-avatar-big);
  display: flex;
  align-items: center;
  justify-content: center;
}

.disabled {
  opacity: 0.5;
  pointer-events: none;
}

.coming-soon-badge {
  padding: 4px 8px;
  background-color: var(--color-bg-primary);
  border-radius: var(--size-border-radius-small);
  color: var(--color-text-secondary);
  margin-right: 8px;
}
</style>
