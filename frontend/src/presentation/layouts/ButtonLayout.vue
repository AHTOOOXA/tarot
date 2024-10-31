<script setup lang="ts">
  import { useButtonStore } from '@/store/button';
  import { storeToRefs } from 'pinia';

  const buttonStore = useButtonStore();
  const { text, isVisible, isLoading } = storeToRefs(buttonStore);
</script>

<template>
  <div class="button-layout">
    <div
      class="app-content"
      :class="{ 'with-navigation': isVisible }"
    >
      <slot></slot>
    </div>

    <div
      v-if="isVisible"
      class="navigation-button"
    >
      <button
        class="primary-button"
        :disabled="isLoading"
        @click="buttonStore.handleClick"
      >
        {{ text }}
      </button>
    </div>
  </div>
</template>

<style scoped>
  .button-layout {
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

  @media (min-width: 460px) {
    .navigation-button {
      max-width: 390px;
      left: 50%;
      transform: translateX(-50%);
    }
  }
</style>
