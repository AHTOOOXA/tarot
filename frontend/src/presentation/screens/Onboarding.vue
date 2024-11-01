<script setup lang="ts">
  import { ref, onMounted } from 'vue';
  import { useRouter } from 'vue-router';
  import { Placeholder, Section, Sections, WithButton } from '@/presentation/components';
  import { useUserStore } from '@/store/user';

  const router = useRouter();
  const userStore = useUserStore();

  const isLoading = ref(true);
  const error = ref<string | null>(null);
  const onboardingSteps = ref<string[]>([]);
  const isButtonLoading = ref(false);

  const user = userStore.user;

  onMounted(async () => {
    try {
      isLoading.value = true;
      onboardingSteps.value = [`Welcome ${user?.first_name}!`, "Let's get you started"];
    } catch (e) {
      error.value = 'Failed to load onboarding steps. Please try again later.';
      console.error('Error loading onboarding steps:', e);
    } finally {
      isLoading.value = false;
    }
  });

  const handleStart = async () => {
    try {
      isButtonLoading.value = true;
      await userStore.onboardUser();
      router.push({ name: 'questions' });
    } catch (error) {
      console.error('Failed to complete onboarding:', error);
    } finally {
      isButtonLoading.value = false;
    }
  };
</script>

<template>
  <WithButton withPadding>
    <template #content>
      <div class="onboarding-page">
        <div
          v-if="isLoading"
          class="loading"
        >
          Loading onboarding...
        </div>
        <div
          v-else-if="error"
          class="error"
        >
          {{ error }}
        </div>
        <Sections v-else>
          <Section standalone>
            <Placeholder
              title="Welcome to Glow App!"
              caption="Let's get started with your onboarding"
            >
              <template #picture>
                <div class="onboarding-icon">🚀</div>
              </template>
            </Placeholder>
          </Section>
          <Section padded>
            <div class="onboarding-content">
              <div
                v-for="(step, index) in onboardingSteps"
                :key="index"
                class="onboarding-step"
              >
                {{ step }}
              </div>
            </div>
          </Section>
        </Sections>
      </div>
    </template>

    <template #button>
      <button
        class="primary-button"
        :disabled="isButtonLoading"
        @click="handleStart"
      >
        Start Using Glow App
      </button>
    </template>
  </WithButton>
</template>

<style scoped>
  .onboarding-page {
    display: flex;
    flex-direction: column;
    min-height: 100%;
  }

  .onboarding-icon {
    font-size: 48px;
    width: var(--size-avatar-big);
    height: var(--size-avatar-big);
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .onboarding-content {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-10);
  }

  .onboarding-step {
    padding: var(--spacing-10);
    background-color: var(--color-bg-tertiary);
    border-radius: var(--size-border-radius-medium);
  }

  .primary-button {
    width: 100%;
    padding: 16px;
    background-color: #4caf50;
    color: white;
    border: none;
    border-radius: 8px;
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
