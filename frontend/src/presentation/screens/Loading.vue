<script setup lang="ts">
defineProps<{
  message?: string;
}>();
</script>

<template>
  <div class="loading-screen">
    <div class="loading-content">
      <div class="loading-icon">🔮</div>
      <div class="loading-text">
        {{ message || 'Loading' }}<span class="dots"><span>.</span><span>.</span><span>.</span></span>
      </div>
    </div>
  </div>
</template>

<style scoped lang="postcss">
@import '@/presentation/styles/theme/typescale.css';

.loading-screen {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: var(--color-bg-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.loading-content {
  text-align: center;
  margin-bottom: 30vh;
}

.loading-icon {
  font-size: 48px;
  margin-bottom: 16px;
  animation: pulse 1.5s infinite;
}

.loading-text {
  @apply --body;
}

@keyframes pulse {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.2);
  }
  100% {
    transform: scale(1);
  }
}

.dots span {
  animation: dots 1.5s infinite;
  opacity: 0;
  display: inline-block;
}

.dots span:nth-child(1) {
  animation-delay: 0s;
}
.dots span:nth-child(2) {
  animation-delay: 0.5s;
}
.dots span:nth-child(3) {
  animation-delay: 1s;
}

@keyframes dots {
  0%,
  100% {
    opacity: 0;
  }
  50% {
    opacity: 1;
  }
}
</style>
