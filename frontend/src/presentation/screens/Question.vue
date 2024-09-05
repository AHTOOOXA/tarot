<script setup lang="ts">
import { ref } from 'vue'
import { useTelegram } from '@/application/services'
import { Placeholder, Section, Sections } from '@/presentation/components'

const question = ref('What is the capital of France?')
const answers = ref(['London', 'Berlin', 'Paris', 'Madrid'])
const { showAlert } = useTelegram()

const selectAnswer = (index: number) => {
  showAlert(`You selected: ${answers.value[index]}`)
  // Add logic here to handle the answer selection
}
</script>

<template>
  <div class="question-page">
    <Sections>
      <Section standalone>
        <Placeholder
          :title="question"
          caption="Choose the correct answer"
          standalone
        >
          <template #picture>
            <div class="question-icon">❓</div>
          </template>
        </Placeholder>
      </Section>
      <Section padded>
        <div class="answer-grid">
          <button
            v-for="(answer, index) in answers"
            :key="index"
            class="answer-button"
            @click="selectAnswer(index)"
          >
            {{ answer }}
          </button>
        </div>
      </Section>
    </Sections>
  </div>
</template>

<style scoped>
.question-page {
  display: flex;
  flex-direction: column;
  min-height: 100%;
  transform: translateZ(0);
}

.question-icon {
  font-size: 48px;
  width: var(--size-avatar-big);
  height: var(--size-avatar-big);
  display: flex;
  align-items: center;
  justify-content: center;
}

.answer-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-10);
}

.answer-button {
  padding: var(--spacing-10);
  background-color: var(--color-bg-tertiary);
  border: none;
  border-radius: var(--size-border-radius-medium);
  color: var(--color-text);
  font-size: 16px;
  text-align: center;
  cursor: pointer;
  transition: background-color 0.2s ease;
  height: 100px;
}

.answer-button:hover {
  background-color: var(--color-bg-quarternary);
}
</style>
