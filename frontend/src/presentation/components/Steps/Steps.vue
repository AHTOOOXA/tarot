<script setup lang="ts">
  interface Props {
    /** Total number of steps */
    count: number;
    /** Current progress (0-indexed) */
    progress: number;
    /** Optional class name */
    customClass?: string;
  }

  defineProps<Props>();
</script>

<template>
  <div :class="['steps-wrapper', customClass]">
    <div
      v-for="i in count"
      :key="i"
      :class="['step', { 'step--active': i - 1 < progress }]"
    />
  </div>
</template>

<style scoped>
  .steps-wrapper {
    display: flex;
    gap: 8px;
    align-items: center;
  }

  .step {
    flex: 1;
    height: 4px;
    background: var(--color-gray-200, #e5e7eb);
    border-radius: var(--size-border-radius-small);
    transition: background-color 0.2s ease;
  }

  .step--active {
    background: var(--color-primary, #4caf50);
  }
</style>
