<script setup lang="ts">
  interface Props {
    currentStep: number;
    totalSteps: number;
  }

  const props = defineProps<Props>();
</script>

<template>
  <div class="progress-container">
    <div class="dots">
      <div
        v-for="step in totalSteps"
        :key="step"
        class="dot"
        :class="{ active: step <= props.currentStep }"
      />
    </div>
  </div>
</template>

<style scoped>
  .progress-container {
    padding: 0 var(--spacing-16);
    position: relative;
    width: 80px;
    margin: 0 auto;
  }

  .dots {
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: relative;
    gap: 12px;
  }

  .dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background-color: grey;
    transition: all 0.3s ease;
  }

  .dot.active {
    background-color: white;
    transform: scale(1.2);
  }
</style>
