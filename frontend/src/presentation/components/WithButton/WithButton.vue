<script setup lang="ts">
defineProps<{
  buttonText?: string;
  buttonDisabled?: boolean;
  buttonClick?: () => void;
}>();
</script>

<template>
  <div class="with-button">
    <div class="with-button__content">
      <slot />
    </div>

    <div class="with-button__footer">
      <button
        class="button button--primary"
        :disabled="buttonDisabled"
        @click="buttonClick?.()"
      >
        {{ buttonText }}
      </button>
    </div>
  </div>
</template>

<style scoped lang="postcss">
@import '@/presentation/styles/theme/typescale.css';

.with-button {
  --footer-padding: 4px 16px 32px 16px;
  --button-height: 56px;
  --desktop-max-width: 390px;
  --footer-height: calc(4px + 32px + var(--button-height));

  display: flex;
  flex-direction: column;
  min-height: 100%;
  position: relative;

  &__content {
    flex: 1;
    overflow-y: auto;
  }

  &__footer {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    padding: var(--footer-padding);

    @media (min-width: 460px) {
      max-width: var(--desktop-max-width);
      left: 50%;
      transform: translateX(-50%);
    }
  }
}

.button {
  width: 100%;
  height: var(--button-height);
  border: none;
  border-radius: var(--size-border-radius-medium);
  transition: all 0.2s ease;
  cursor: pointer;
  touch-action: manipulation;
  display: flex;
  align-items: center;
  justify-content: center;

  @apply --body-semibold;

  &--primary {
    background-color: var(--color-primary);
    color: var(--color-text-inverse);

    &:disabled {
      opacity: 0.3;
      cursor: not-allowed;
    }
  }
}
</style>
