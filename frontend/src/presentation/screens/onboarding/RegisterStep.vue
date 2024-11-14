<script setup lang="ts">
  import { ref } from 'vue';
  import { Placeholder, Section } from '@/presentation/components';

  const step = {
    title: 'Complete Your Profile',
    subtitle: 'Tell us a bit about yourself',
    icon: '📝',
  } as const;

  const form = ref({
    name: '',
    email: '',
  });
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
    <form
      class="register-form"
      @submit.prevent
    >
      <input
        v-model="form.name"
        type="text"
        placeholder="Your name"
        class="form-input"
      />
      <input
        v-model="form.email"
        type="email"
        placeholder="Your email"
        class="form-input"
      />
    </form>
  </Section>
</template>

<style scoped>
  .register-form {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-10);
    margin-top: var(--spacing-20);
  }

  .form-input {
    padding: var(--spacing-10);
    border: 1px solid var(--color-border);
    border-radius: var(--size-border-radius-medium);
    font-size: 16px;
  }
</style>
