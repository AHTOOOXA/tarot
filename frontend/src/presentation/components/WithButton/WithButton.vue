<script setup lang="ts">
  defineProps<{
    withPadding?: boolean;
  }>();
</script>

<template>
  <div class="with-button">
    <div
      class="content"
      :class="{ 'with-padding': withPadding }"
    >
      <slot name="content"></slot>
    </div>

    <div class="button-container">
      <slot name="button"></slot>
    </div>
  </div>
</template>

<style scoped>
  .with-button {
    display: flex;
    flex-direction: column;
    min-height: 100%;
    position: relative;
  }

  .content {
    flex: 1;
    overflow-y: auto;
  }

  .content.with-padding {
    padding-bottom: 70px;
  }

  .button-container {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    padding: 35px 16px;
    background-color: var(--color-bg-secondary);
    box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
  }

  @media (min-width: 460px) {
    .button-container {
      max-width: 390px;
      left: 50%;
      transform: translateX(-50%);
    }
  }
</style>
