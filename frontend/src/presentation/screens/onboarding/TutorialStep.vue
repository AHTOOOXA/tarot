<script setup lang="ts">
  import { Placeholder, Section } from '@/presentation/components';

  const step = {
    title: 'Quick Tutorial',
    subtitle: 'Learn how to use Glow App',
    icon: '🎓',
  } as const;

  const tutorialPoints = ['Track your progress daily', 'Set and achieve goals', 'Connect with others'] as const;
</script>

<template>
  <Section>
    <Placeholder
      :title="step.title"
      :caption="step.subtitle"
    >
      <template #picture>
        <div class="step-icon">{{ step.icon }}</div>
      </template>
    </Placeholder>
    <div class="tutorial-points">
      <div
        v-for="(point, index) in tutorialPoints"
        :key="index"
        class="tutorial-point"
      >
        <span class="point-number">{{ index + 1 }}</span>
        <span>{{ point }}</span>
      </div>
    </div>
  </Section>
</template>

<style scoped>
  .tutorial-points {
    margin-top: var(--spacing-20);
    display: flex;
    flex-direction: column;
    gap: var(--spacing-10);
  }

  .tutorial-point {
    display: flex;
    align-items: center;
    gap: var(--spacing-10);
    padding: var(--spacing-10);
    background-color: var(--color-bg-tertiary);
    border-radius: var(--size-border-radius-medium);
  }

  .point-number {
    background-color: var(--color-primary);
    color: white;
    width: 24px;
    height: 24px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
  }
</style>
