<script setup lang="ts">
import { computed, onBeforeMount, onErrorCaptured } from 'vue';
import { useRoute } from 'vue-router';
import { useTelegram } from '@/services';
import BaseLayout from '@/presentation/layouts/BaseLayout.vue';
import TabsLayout from '@/presentation/layouts/TabsLayout.vue';

const { colorScheme, expand } = useTelegram();
const route = useRoute();

const layoutComponent = computed(() => {
  switch (route.meta.layout) {
    case 'tabs':
      return TabsLayout;
    default:
      return BaseLayout;
  }
});

function onBeforeSegue(): void {
  requestAnimationFrame(() => {
    window.scrollTo(0, 0);
  });
}

onErrorCaptured((error: Error) => {
  console.error(error);
});

onBeforeMount(async () => {
  if (colorScheme !== undefined) {
    document.body.classList.add(colorScheme);
  }
  expand();
});
</script>

<template>
  <div class="app">
    <component :is="layoutComponent">
      <div class="container">
        <RouterView v-slot="{ Component }">
          <transition
            name="default-segue"
            @before-enter="onBeforeSegue"
          >
            <component :is="Component" />
          </transition>
        </RouterView>
      </div>
    </component>
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
}

.container {
  padding: 16px;
  width: 100%;
  margin: 0 auto;
  box-sizing: border-box;
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
</style>
