<script setup lang="ts">
import { ref, onBeforeMount, onErrorCaptured } from 'vue'
import { useTelegram } from '@/application/services'

const { colorScheme, expand } = useTelegram()

/**
 * Hook will be called when next screen just added to the DOM
 * We use it to scroll to the top of the page
 */
function onBeforeSegue(): void {
  requestAnimationFrame(() => {
    window.scrollTo(0, 0)
  })
}

onErrorCaptured((error: Error) => {
  console.error(error)
})

onBeforeMount(() => {
  if (colorScheme !== undefined) {
    document.body.classList.add(colorScheme)
  }
  expand()
})

const activeTab = ref('Questions') // Default active tab

const tabs = [
  { name: 'Inbox', icon: '📥' },
  { name: 'Questions', icon: '❓' },
  { name: 'Friends', icon: '👥' },
  { name: 'Profile', icon: '👤' },
]

function changeTab(tabName: string) {
  activeTab.value = tabName
  // Here you would typically handle navigation to the corresponding route
  // For example: router.push({ name: tabName.toLowerCase() })
}
</script>

<template>
  <div class="app">
    <div class="app-content">
      <div class="app-header"></div><!--Teleport location for PageWithHeader component-->
      <RouterView v-slot="{ Component }">
        <transition
          name="default-segue"
          @before-enter="onBeforeSegue"
        >
          <component :is="Component" />
        </transition>
      </RouterView>
    </div>
    <nav class="tab-menu">
      <button 
        v-for="tab in tabs" 
        :key="tab.name"
        @click="changeTab(tab.name)"
        :class="{ active: activeTab === tab.name }"
        class="tab-button"
      >
        <span class="tab-icon">{{ tab.icon }}</span>
        <span class="tab-name">{{ tab.name }}</span>
      </button>
    </nav>
  </div>
</template>

<style>
@import '@/presentation/styles/theme/typescale.css';

:root {
  color-scheme: light dark;
}

body {
  margin: 0;
  display: flex;
  min-width: 320px;
  min-height: 100vh;
  background-color: var(--color-bg-secondary);
  overflow: hidden; /* Prevent scrolling on the body */
}

#app {
  display: flex;
  flex-direction: column;
  height: 100vh; /* Full viewport height */
  width: 100%;
  font-family: var(--family);
  overflow: hidden; /* Prevent scrolling on the app container */

  font-synthesis: none;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  -webkit-text-size-adjust: 100%;

  @media (min-width: 460px) {
    max-width: 390px;
    margin: 0 auto;
  }
}

.app {
  display: flex;
  flex-direction: column;
  height: 100%;
  color: var(--color-text);
  position: relative;
  user-select: none;
  padding-bottom: 60px; /* Add padding to accommodate the tab menu */
}

.app-content {
  flex: 1;
  overflow-y: auto; /* Allow scrolling within the content area */
  padding-bottom: 70px; /* Increased padding to accommodate the tab menu */
}

.app-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
}

.default-segue-leave-active {
  visibility: hidden;
  height: 0;
  overflow: hidden;
}

.default-segue-enter-active {
  transition: opacity 500ms ease;
  will-change: opacity;
}

.default-segue-enter-from,
.default-segue-leave-to {
  opacity: 0;
}

.tab-menu {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  justify-content: space-around;
  background-color: var(--color-bg-secondary);
  padding: 25px 0; /* Increased padding for more space */
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

@media (min-width: 460px) {
  #app {
    max-width: 390px;
    margin: 0 auto;
  }

  .tab-menu {
    max-width: 390px;
    left: 50%;
    transform: translateX(-50%);
  }
}
</style>
