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
    <div class="app-content">
      <slot></slot>
    </div>

    <nav class="tab-menu">
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
  </div>
</template>

<style scoped>
.tabs-layout {
  display: flex;
  flex-direction: column;
  height: 100%;
  position: relative;
}

.app-content {
  flex: 1;
  overflow-y: auto;
  padding-bottom: 70px;
}

.tab-menu {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: var(--color-bg-secondary);
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-around;
  padding: 16px;
}

.tab-button {
  background: none;
  border: none;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: color 0.2s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.tab-button.active {
  color: #4caf50;
}

.tab-icon {
  font-size: 24px;
  margin-bottom: 8px;
}

.tab-name {
  font-size: 12px;
}

@media (min-width: 460px) {
  .tab-menu {
    max-width: 390px;
    left: 50%;
    transform: translateX(-50%);
  }
}
</style>
