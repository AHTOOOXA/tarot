<script setup lang="ts"></script>

<template>
  <div class="base-layout">
    <div class="app-content">
      <slot></slot>
    </div>
  </div>
</template>

<style scoped>
  .base-layout {
    display: flex;
    flex-direction: column;
    height: 100%;
    position: relative;
  }

  .app-content {
    flex: 1;
    overflow-y: auto;
  }
</style>
