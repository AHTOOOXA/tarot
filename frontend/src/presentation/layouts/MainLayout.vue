<script setup lang="ts">
  import { computed } from 'vue';
  import { useRoute } from 'vue-router';

  const route = useRoute();
  const showTabMenu = computed(() => !route.meta.hideTabMenu);

  const tabs = [
    { name: 'Inbox', icon: '📥', route: 'inbox' },
    { name: 'Questions', icon: '❓', route: 'questions' },
    { name: 'Friends', icon: '👥', route: 'friends' },
    { name: 'Profile', icon: '👤', route: 'profile' },
  ];
</script>

<template>
  <div class="main-layout">
    <div
      class="app-content"
      :class="{ 'with-tab-menu': showTabMenu }"
    >
      <slot></slot>
    </div>

    <nav
      v-if="showTabMenu"
      class="tab-menu"
    >
      <button
        v-for="tab in tabs"
        :key="tab.name"
        :to="{ name: tab.route }"
        :class="{ active: $route.name === tab.route }"
        class="tab-button"
      >
        <span class="tab-icon">{{ tab.icon }}</span>
        <span class="tab-name">{{ tab.name }}</span>
      </button>
    </nav>
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

  .app-content.with-tab-menu {
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

  /* Rest of the styles from your original App.vue tab-menu styles */
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

  @media (min-width: 460px) {
    .tab-menu {
      max-width: 390px;
      left: 50%;
      transform: translateX(-50%);
    }
  }
</style>
