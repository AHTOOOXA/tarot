<script setup lang="ts">
  import { ref, computed } from 'vue';
  import { useRouter } from 'vue-router';
  import { WithButton, Sections } from '@/presentation/components';
  import Steps from '@/presentation/components/Steps/Steps.vue';
  import { useUserStore } from '@/store/user';
  import HelloStep from './onboarding/HelloStep.vue';
  import RegisterStep from './onboarding/RegisterStep.vue';
  import TutorialStep from './onboarding/TutorialStep.vue';

  const STEPS = [
    { component: HelloStep, buttonText: 'Get Started' },
    { component: RegisterStep, buttonText: 'Continue' },
    { component: TutorialStep, buttonText: 'Complete Onboarding' },
  ] as const;

  const router = useRouter();
  const userStore = useUserStore();
  const currentStepIndex = ref(0);

  const currentComponent = computed(() => STEPS[currentStepIndex.value].component);
  const buttonText = computed(() => STEPS[currentStepIndex.value].buttonText);
  const isLastStep = computed(() => currentStepIndex.value === STEPS.length - 1);

  const handleNext = async () => {
    if (isLastStep.value) {
      await completeOnboarding();
      return;
    }
    currentStepIndex.value++;
  };

  const completeOnboarding = async () => {
    try {
      await userStore.onboardUser();
      router.push({ name: 'questions' });
    } catch (error) {
      console.error('Failed to complete onboarding:', error);
    }
  };
</script>

<template>
  <WithButton withPadding>
    <template #content>
      <Steps
        :count="STEPS.length"
        :progress="currentStepIndex + 1"
        custom-class="steps"
      />
      <Sections class="sections-container">
        <component :is="currentComponent" />
      </Sections>
    </template>

    <template #button>
      <button
        class="primary-button"
        @click="handleNext"
      >
        {{ buttonText }}
      </button>
    </template>
  </WithButton>
</template>

<style scoped>
  .sections-container {
    margin-top: var(--spacing-8);
  }

  .primary-button {
    width: 100%;
    padding: 16px;
    background-color: var(--color-primary);
    color: white;
    border: none;
    border-radius: var(--size-border-radius-medium);
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    transition: background-color 0.2s ease;
  }

  .primary-button:disabled {
    opacity: 0.7;
    cursor: not-allowed;
  }
</style>
