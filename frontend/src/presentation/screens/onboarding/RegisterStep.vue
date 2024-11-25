<script setup lang="ts">
import { ref, computed } from 'vue';
import { Placeholder, Section, WithButton, Input, List } from '@/presentation/components';

const emit = defineEmits<{
  'step-complete': [];
}>();

const step = {
  title: 'Complete Your Profile',
  subtitle: 'Tell us a bit about yourself',
  icon: '📝',
} as const;

const form = ref({
  name: '',
  email: '',
});

const isButtonDisabled = computed(() => {
  return !form.value.name.trim() || !form.value.email.trim();
});

const handleClick = () => {
  emit('step-complete');
};
</script>

<template>
  <WithButton
    button-text="Continue"
    :button-disabled="isButtonDisabled"
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
        <Input
          v-model="form.name"
          placeholder="Your name"
        />
        <Input
          v-model="form.email"
          placeholder="Your email"
        />
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
</style>
