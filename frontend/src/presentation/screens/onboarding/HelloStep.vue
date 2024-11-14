<script setup lang="ts">
  import { Placeholder, Section } from '@/presentation/components';

  const step = {
    title: 'Welcome to Glow App!',
    subtitle: "We're excited to have you here. Let's get you started!",
    icon: '👋',
  } as const;
</script>

<template>
  <Section standalone>
    <Placeholder
      :title="step.title"
      :caption="step.subtitle"
    >
      <template #picture>
        <div class="step-icon">{{ step.icon }}</div>
      </template>
    </Placeholder>
  </Section>
</template>

<style scoped>
  .step-icon {
    font-size: 48px;
    width: var(--size-avatar-big);
    height: var(--size-avatar-big);
    display: flex;
    align-items: center;
    justify-content: center;
  }
</style>
