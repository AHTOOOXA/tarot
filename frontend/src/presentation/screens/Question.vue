<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useTelegram } from '@/application/services'
import { useQuestions } from '@/domain/services/useQuestions'
import { Placeholder, Section, Sections } from '@/presentation/components'

const { questions, load } = useQuestions()
const currentQuestionIndex = ref(0)
const { showAlert } = useTelegram()
const isLoading = ref(true)
const error = ref<string | null>(null)

const selectAnswer = (answer: string) => {
  showAlert(`You selected: ${answer}`)
  if (currentQuestionIndex.value < questions.value.length - 1) {
    currentQuestionIndex.value++
  } else {
    showAlert('You have completed all questions!')
  }
}

onMounted(async () => {
  try {
    isLoading.value = true
    await load()
    console.log('Loaded questions:', questions.value)
  } catch (e) {
    error.value = 'Failed to load questions. Please try again later.'
    console.error('Error loading questions:', e)
  } finally {
    isLoading.value = false
  }
})

watch(questions, (newQuestions) => {
  console.log('Questions updated:', newQuestions)
})

const currentQuestion = () => {
  const question = questions.value[currentQuestionIndex.value]
  console.log('Current question:', question)
  return question
}
</script>

<template>
  <div class="question-page">
    <div v-if="isLoading" class="loading">Loading questions...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <Sections v-else-if="questions.length > 0">
      <Section standalone>
        <Placeholder
          :title="currentQuestion().question_text"
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
            v-for="answer in currentQuestion().answers"
            :key="answer.user_id"
            class="answer-button"
            @click="selectAnswer(answer.answer_text)"
          >
            {{ answer.answer_text }}
          </button>
        </div>
      </Section>
    </Sections>
    <div v-else class="no-questions">No questions available.</div>
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

.loading {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  font-size: 18px;
  color: var(--color-text);
}

.error, .no-questions {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  font-size: 18px;
  color: var(--color-text);
}

.error {
  color: var(--color-error);
}
</style>
