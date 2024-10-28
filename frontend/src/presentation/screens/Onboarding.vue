<script setup lang="ts">
  import { ref, onMounted } from 'vue';
  import { useRouter } from 'vue-router';
  import { Placeholder, Section, Sections } from '@/presentation/components';
  import useTelegram from '@/services/useTelegram';
  import { useStart, StartParamKey } from '@/composables/start';
  import { useUserStore } from '@/store/user';

  const router = useRouter();
  const { webAppInitData } = useTelegram();
  const { parseStartParam, getStartParam } = useStart();
  const userStore = useUserStore();

  const isLoading = ref(true);
  const error = ref<string | null>(null);
  const onboardingSteps = ref<string[]>([]);
  const invitedByUser = ref<any>(null);

  onMounted(async () => {
    try {
      isLoading.value = true;
      // Parse webAppInitData to get user information
      const initData = new URLSearchParams(webAppInitData);
      const user = JSON.parse(initData.get('user') || '{}');

      // TODO: redo this and add inviting group / user to start store
      // // Parse start parameters
      // parseStartParam()
      // const friendId = getStartParam(StartParamKey.FRIEND)

      // // if (friendId) {
      // //   // Fetch friend information
      // //   invitedByUser.value = await userStore.fetchUserById(Number(friendId))
      // // }

      // Simulating API call to get onboarding steps
      await new Promise(resolve => setTimeout(resolve, 1000));
      onboardingSteps.value = [`Welcome ${user.first_name}!`, "Let's get you started"];
    } catch (e) {
      error.value = 'Failed to load onboarding steps. Please try again later.';
      console.error('Error loading onboarding steps:', e);
    } finally {
      isLoading.value = false;
    }
  });

  const startApp = () => {
    // Navigate to the friends page
    router.push({ name: 'friends' });
  };
</script>

<template>
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
      <Placeholder
        compact
        v-if="invitedByUser"
        :title="`You were invited by ${invitedByUser.first_name} ${invitedByUser.last_name}`"
        :caption="`@${invitedByUser.username}`"
      >
      </Placeholder>
      <Section padded>
        <div class="onboarding-content">
          <div
            v-for="(step, index) in onboardingSteps"
            :key="index"
            class="onboarding-step"
          >
            {{ step }}
          </div>
          <div
            class="start-button"
            @click="startApp"
          >
            Start Using Glow App
          </div>
        </div>
      </Section>
    </Sections>
  </div>
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

  .start-button {
    padding: var(--spacing-10);
    background-color: #4caf50; /* Green color */
    border-radius: var(--size-border-radius-medium);
    color: white;
    text-align: center;
    font-weight: bold;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }

  .start-button:hover {
    background-color: #45a049; /* Darker green on hover */
  }
</style>
