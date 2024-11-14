<script setup lang="ts">
  import { ref, computed } from 'vue';
  import { useRouter } from 'vue-router';
  import { WithButton, Sections } from '@/presentation/components';
  import ProgressBar from '@/presentation/components/ProgressBar/ProgressBar.vue';
  import { useUserStore } from '@/store/user';
  import HelloStep from './onboarding/HelloStep.vue';
  import RegisterStep from './onboarding/RegisterStep.vue';
  import TutorialStep from './onboarding/TutorialStep.vue';

  const router = useRouter();
  const userStore = useUserStore();

  type StepId = 'hello' | 'register' | 'tutorial';
  const currentStep = ref<StepId>('hello');

  const currentStepIndex = computed(() => {
    const stepMap = {
      hello: 1,
      register: 2,
      tutorial: 3,
    };
    return stepMap[currentStep.value];
  });

  const currentComponent = computed(() => {
    switch (currentStep.value) {
      case 'hello':
        return HelloStep;
      case 'register':
        return RegisterStep;
      case 'tutorial':
        return TutorialStep;
      default:
        return HelloStep;
    }
  });

  const buttonText = computed(() => {
    switch (currentStep.value) {
      case 'hello':
        return 'Get Started';
      case 'register':
        return 'Continue';
      case 'tutorial':
        return 'Complete Onboarding';
      default:
        return 'Next';
    }
  });

  const handleNext = async () => {
    switch (currentStep.value) {
      case 'hello':
        currentStep.value = 'register';
        break;
      case 'register':
        currentStep.value = 'tutorial';
        break;
      case 'tutorial':
        await completeOnboarding();
        break;
    }
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
      <div class="progress-wrapper">
        <ProgressBar
          :current-step="currentStepIndex"
          :total-steps="3"
        />
      </div>
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
  .progress-wrapper {
    padding: 24px 0 8px;
    position: sticky;
    top: 0;
    z-index: 10;
  }

  .sections-container {
    margin-top: var(--spacing-8);
  }

  .primary-button {
    width: 100%;
    padding: 16px;
    background-color: #4caf50;
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
