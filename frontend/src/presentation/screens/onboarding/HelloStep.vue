<script setup lang="ts">
import { ref, computed } from 'vue';
import { Placeholder, Section, Checkbox, WithButton } from '@/presentation/components';
import { useUserStore } from '@/store/user';
import { useStatic } from '@/services/useStatic';

const userStore = useUserStore();
const { getStaticUrl } = useStatic();

const emit = defineEmits<{
  'step-complete': [];
}>();

const step = {
  title: 'Welcome to Tarot App!',
  subtitle: 'Discover insights and guidance through the ancient wisdom of Tarot.',
  icon: '🔮',
} as const;

const termsAccepted = ref(userStore.user?.is_terms_accepted ?? false);
const isButtonDisabled = computed(() => !termsAccepted.value);

const handleClick = () => {
  userStore.setTermsAccepted();
  emit('step-complete');
};

const termsUrl = getStaticUrl('oferta-tarot.pdf');
const privacyUrl = getStaticUrl('privacy-policy.pdf'); // TODO: add privacy policy
</script>

<!-- TODO: REDO layout make proper bottom sticking -->
<template>
  <WithButton
    button-text="Get Started"
    :button-disabled="isButtonDisabled"
    :button-click="handleClick"
  >
    <Section
      standalone
      class="hello-step"
    >
      <div class="content">
        <Placeholder
          :title="step.title"
          :caption="step.subtitle"
        >
          <template #picture>
            <div class="step-icon">{{ step.icon }}</div>
          </template>
        </Placeholder>
      </div>

      <div
        v-show="!userStore.user?.is_terms_accepted"
        class="terms-container"
      >
        <Checkbox v-model="termsAccepted">
          I accept the
          <a
            :href="termsUrl"
            target="_blank"
            class="terms-link"
          >
            Terms of Service
          </a>
          and
          <a
            :href="privacyUrl"
            target="_blank"
            class="terms-link"
          >
            Privacy Policy
          </a>
        </Checkbox>
      </div>
    </Section>
  </WithButton>
</template>

<style scoped lang="postcss">
.hello-step {
  display: flex;
  flex-direction: column;
  min-height: calc(100vh - 32px - var(--footer-height));
}

.content {
  flex: 1;
}

.terms-container {
  margin-bottom: var(--spacing-16);
}

.step-icon {
  font-size: 48px;
  width: var(--size-avatar-big);
  height: var(--size-avatar-big);
  display: flex;
  align-items: center;
  justify-content: center;
}

.terms-link {
  color: var(--color-primary);
  text-decoration: underline;
}
</style>
