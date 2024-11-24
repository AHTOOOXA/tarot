<script setup lang="ts">
  const props = defineProps<{
    modelValue: boolean;
    label?: string;
    disabled?: boolean;
  }>();

  const emit = defineEmits<{
    'update:modelValue': [value: boolean];
  }>();

  const toggle = () => {
    if (!props.disabled) {
      emit('update:modelValue', !props.modelValue);
    }
  };
</script>

<template>
  <div
    class="checkbox"
    :class="{ disabled }"
    @click="toggle"
  >
    <div
      class="checkbox-box"
      :class="{ checked: modelValue }"
    >
      <svg
        v-if="modelValue"
        viewBox="0 0 24 24"
        class="check-icon"
      >
        <path
          d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41L9 16.17z"
          fill="currentColor"
          stroke="currentColor"
          stroke-width="0.5"
        />
      </svg>
    </div>
    <span
      v-if="label"
      class="label"
      >{{ label }}</span
    >
  </div>
</template>

<style scoped lang="postcss">
  @import '@/presentation/styles/theme/typescale.css';

  .checkbox {
    --check-size: 24px;
    --icon-size: 16px;

    display: flex;
    align-items: center;
    gap: var(--spacing-10);
    cursor: pointer;
    user-select: none;

    @apply --body;

    &.disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }

    .checkbox-box {
      width: var(--check-size);
      height: var(--check-size);
      border: 2px solid var(--color-primary);
      border-radius: var(--size-border-radius-small);
      display: flex;
      align-items: center;
      justify-content: center;
      transition: background-color 200ms ease;
      flex-shrink: 0;

      &.checked {
        background-color: var(--color-primary);
      }
    }

    .check-icon {
      width: var(--icon-size);
      height: var(--icon-size);
      color: var(--color-text);
    }

    .label {
      color: var(--color-hint);
    }
  }
</style>
