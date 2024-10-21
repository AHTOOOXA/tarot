<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useQuizzes } from '@/domain/services/useQuizzes'
import { Placeholder, Section, Sections } from '@/presentation/components'

const { quizzes, load, submitQuizResponse } = useQuizzes()
const currentQuizIndex = ref(0)
const isLoading = ref(true)
const error = ref<string | null>(null)
const selectedAnswerId = ref<number | null>(null)

const selectAnswer = async (answerId: number) => {
  selectedAnswerId.value = answerId
  console.log('Selected answer:', answerId)

  // Start the API request without awaiting it
  submitQuizResponse({
    question_id: currentQuiz().question.id,
    answer_id: answerId
  }).catch(error => {
    console.error('Failed to submit quiz response:', error)
    // Optionally, show an error message to the user
  })

  // Wait for the animation to complete
  await new Promise(resolve => setTimeout(resolve, 300))

  if (currentQuizIndex.value < quizzes.value.length - 1) {
    currentQuizIndex.value++
  } else {
    // Handle end of questions if needed
  }

  // Reset the selected answer
  selectedAnswerId.value = null
}

onMounted(async () => {
  try {
    isLoading.value = true
    await load()
    console.log('Loaded quizzes:', quizzes.value)
  } catch (e) {
    error.value = 'Failed to load quizzes. Please try again later.'
    console.error('Error loading questions:', e)
  } finally {
    isLoading.value = false
  }
})

watch(quizzes, (newQuizzes) => {
  console.log('Quizzes updated:', newQuizzes)
})

const currentQuiz = () => {
  const quiz = quizzes.value[currentQuizIndex.value]
  console.log('Current quiz:', quiz)
  return quiz
}
</script>

<template>
  <div class="question-page">
    <div v-if="isLoading" class="loading">Loading questions...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <Sections v-else-if="quizzes.length > 0">
      <Section standalone>
        <Placeholder
          :title="currentQuiz().question.text"
          caption="чиназес"
          standalone
        >
          <template #picture>
            <div class="question-emoji">{{ currentQuiz().question.emoji }}</div>
          </template>
        </Placeholder>
      </Section>
      <Section padded>
        <div class="answer-grid">
          <button
            v-for="friend in currentQuiz().friends"
            :key="friend.id"
            class="answer-button"
            :class="{ 'selected': selectedAnswerId === friend.id }"
            @click="selectAnswer(friend.id)"
          >
            {{ friend.first_name + ' ' + friend.last_name || friend.username }}
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

.question-emoji {
  font-size: 48px;
  width: var(--size-avatar-big) * 3;
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
  height: 100px;
}

.answer-button.selected {
  animation: selectAnimation 0.3s ease-in forwards;
}

@keyframes selectAnimation {
  to {
    background-color: var(--color-success, #4CAF50);
    transform: scale(1.1);
  }
}
</style>
