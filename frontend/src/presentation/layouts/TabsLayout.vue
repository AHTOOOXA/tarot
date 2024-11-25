<script setup lang="ts">
import { useRouter } from 'vue-router';

const router = useRouter();

const tabs = [
  { name: 'Inbox', icon: '📥', route: 'inbox' },
  { name: 'Questions', icon: '❓', route: 'questions' },
  { name: 'Friends', icon: '👥', route: 'friends' },
  { name: 'Profile', icon: '👤', route: 'profile' },
];

const navigateToRoute = (routeName: string) => {
  router.push({ name: routeName });
};
</script>

<template>
  <div class="tabs-layout">
    <div class="tabs-layout__content">
      <slot />
    </div>

    <nav class="tabs-layout__footer">
      <button
        v-for="tab in tabs"
        :key="tab.name"
        :class="{ active: $route.name === tab.route }"
        class="tab-button"
        @click="navigateToRoute(tab.route)"
      >
        <span class="tab-button__icon">{{ tab.icon }}</span>
        <span class="tab-button__name">{{ tab.name }}</span>
      </button>
    </nav>
  </div>
</template>

<style scoped lang="postcss">
@import '@/presentation/styles/theme/typescale.css';

.tabs-layout {
  --footer-padding: 8px 16px 28px 16px;
  --tabs-height: 56px;
  --footer-height: calc(8px + 28px + var(--tabs-height));
  --desktop-max-width: 390px;

  display: flex;
  flex-direction: column;
  min-height: 100%;
  position: relative;

  &__content {
    flex: 1;
    overflow-y: auto;
    padding-bottom: var(--footer-height);
  }

  &__footer {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    min-height: var(--tabs-height);
    padding: var(--footer-padding);
    background-color: var(--color-bg-secondary);
    box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.2);
    display: flex;
    justify-content: space-around;
    box-sizing: border-box;

    @media (min-width: 460px) {
      max-width: var(--desktop-max-width);
      left: 50%;
      transform: translateX(-50%);
    }
  }
}

.tab-button {
  cursor: pointer;
  transition: color 0.2s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
  color: var(--color-text-secondary);

  @apply --footer;

  &.active {
    color: var(--color-primary);
  }

  &__icon {
    font-size: 28px;
    margin-bottom: 4px;
  }

  &__name {
    font-size: 12px;
  }
}
</style>
