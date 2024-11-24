<script setup lang="ts">
  import { ref, computed } from 'vue';
  import { useRouter } from 'vue-router';
  import { WithButton, Sections } from '@/presentation/components';
  import Steps from '@/presentation/components/Steps/Steps.vue';
  import { useUserStore } from '@/store/user';
  import HelloStep from './onboarding/HelloStep.vue';
  import RegisterStep from './onboarding/RegisterStep.vue';
  import TutorialStep from './onboarding/TutorialStep.vue';

  const STEPS = [{ component: HelloStep }, { component: RegisterStep }, { component: TutorialStep }] as const;

  const router = useRouter();
  const userStore = useUserStore();
  const currentStepIndex = ref(0);
  const currentComponent = computed(() => STEPS[currentStepIndex.value].component);
  const isLastStep = computed(() => currentStepIndex.value === STEPS.length - 1);

  const handleStepComplete = async () => {
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
  <Steps
    :count="STEPS.length"
    :progress="currentStepIndex + 1"
    custom-class="steps"
  />
  <component
    :is="currentComponent"
    @step-complete="handleStepComplete"
  />
</template>

<style scoped>
  .sections-container {
    margin-top: var(--spacing-8);
  }
</style>
