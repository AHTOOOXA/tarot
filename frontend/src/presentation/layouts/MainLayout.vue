<script setup lang="ts">
  import { computed } from 'vue';
  import { useRoute, useRouter } from 'vue-router';

  const route = useRoute();
  const router = useRouter();

  const navigationMode = computed(() => route.meta.navigationMode);

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
  <div class="main-layout">
    <div
      class="app-content"
      :class="{
        'with-navigation': navigationMode !== 'none',
      }"
    >
      <slot></slot>
    </div>

    <!-- Tab Menu Navigation -->
    <nav
      v-if="navigationMode === 'tabs'"
      class="tab-menu"
    >
      <button
        v-for="tab in tabs"
        :key="tab.name"
        :class="{ active: $route.name === tab.route }"
        class="tab-button"
        @click="navigateToRoute(tab.route)"
      >
        <span class="tab-icon">{{ tab.icon }}</span>
        <span class="tab-name">{{ tab.name }}</span>
      </button>
    </nav>

    <!-- Button Navigation -->
    <div
      v-if="navigationMode === 'button'"
      class="navigation-button"
    >
      <button
        class="primary-button"
        @click="navigateToRoute('questions')"
      >
        Continue
      </button>
    </div>
  </div>
</template>

<style scoped>
  .main-layout {
    display: flex;
    flex-direction: column;
    height: 100%;
    position: relative;
  }

  .app-content {
    flex: 1;
    overflow-y: auto;
  }

  .app-content.with-navigation {
    padding-bottom: 70px;
  }

  .tab-menu {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    display: flex;
    justify-content: space-around;
    background-color: var(--color-bg-secondary);
    padding: 25px 0;
    box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
  }

  .tab-button {
    display: flex;
    flex-direction: column;
    align-items: center;
    background: none;
    border: none;
    color: var(--color-text);
    font-size: 12px;
    cursor: pointer;
    padding: 5px;
  }

  .tab-button.active {
    color: var(--color-primary);
  }

  .tab-icon {
    font-size: 24px;
    margin-bottom: 2px;
  }

  .tab-name {
    font-size: 10px;
  }

  .navigation-button {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    padding: 35px 16px;
    background-color: var(--color-bg-secondary);
    box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
  }

  .primary-button {
    width: 100%;
    padding: 16px;
    /* background-color: var(--color-primary); */
    background-color: green;
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    transition: background-color 0.2s ease;
  }

  .primary-button:hover {
    background-color: var(--color-primary-dark);
  }

  @media (min-width: 460px) {
    .tab-menu,
    .navigation-button {
      max-width: 390px;
      left: 50%;
      transform: translateX(-50%);
    }
  }
</style>
