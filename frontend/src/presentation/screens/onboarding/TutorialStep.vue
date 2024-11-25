<script setup lang="ts">
import { Placeholder, Section, WithButton, List } from '@/presentation/components';

const emit = defineEmits<{
  'step-complete': [];
}>();

const step = {
  title: 'Quick Tutorial',
  subtitle: 'Learn how to use Glow App',
  icon: '🎓',
} as const;

const tutorialPoints = ['Track your progress daily', 'Set and achieve goals', 'Connect with others'] as const;

const handleClick = () => {
  emit('step-complete');
};
</script>

<template>
  <WithButton
    button-text="Get Started"
    :button-click="handleClick"
  >
    <Section standalone>
      <Placeholder
        :title="step.title"
        :caption="step.subtitle"
      >
        <template #picture>
          <div class="step-icon">{{ step.icon }}</div>
        </template>
      </Placeholder>
      <List gapped>
        <div
          v-for="(point, index) in tutorialPoints"
          :key="index"
          class="tutorial-point"
        >
          <span class="point-number">{{ index + 1 }}</span>
          <span>{{ point }}</span>
        </div>
      </List>
    </Section>
  </WithButton>
</template>

<style scoped lang="postcss">
.step-icon {
  font-size: 48px;
  width: var(--size-avatar-big);
  height: var(--size-avatar-big);
  display: flex;
  align-items: center;
  justify-content: center;
}

.tutorial-point {
  display: flex;
  align-items: center;
  gap: var(--spacing-10);
  padding: var(--spacing-10);
  background-color: var(--color-bg-tertiary);
  border-radius: var(--size-border-radius-medium);

  @apply --body;
}

.point-number {
  background-color: var(--color-primary);
  color: var(--color-text-inverse);
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
}
</style>
