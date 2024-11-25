<script setup lang="ts">
import { ref, computed } from 'vue';
import { Placeholder, Section, Checkbox, WithButton } from '@/presentation/components';

const emit = defineEmits<{
  'step-complete': [];
}>();

const step = {
  title: 'Welcome to Tarot App!',
  subtitle: 'Discover insights and guidance through the ancient wisdom of Tarot.',
  icon: '🔮',
} as const;

const termsAccepted = ref(false);
const isButtonDisabled = computed(() => !termsAccepted.value);

const handleClick = () => {
  emit('step-complete');
};
</script>

<template>
  <WithButton
    button-text="Get Started"
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
      <div>
        <Checkbox
          v-model="termsAccepted"
          label="I accept the Terms of Service and Privacy Policy"
        />
      </div>
    </Section>
  </WithButton>
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
