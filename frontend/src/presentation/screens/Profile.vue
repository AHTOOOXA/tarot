<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Placeholder, Section, Sections } from '@/presentation/components'

const isLoading = ref(true)
const error = ref<string | null>(null)
const profile = ref<any | null>(null)

onMounted(async () => {
  try {
    isLoading.value = true
    // Simulating API call
    await new Promise(resolve => setTimeout(resolve, 1000))
    profile.value = {
      name: 'John Doe',
      email: 'john@example.com',
      bio: 'I love answering questions!',
    }
  } catch (e) {
    error.value = 'Failed to load profile. Please try again later.'
    console.error('Error loading profile:', e)
  } finally {
    isLoading.value = false
  }
})
</script>

<template>
  <div class="profile-page">
    <div v-if="isLoading" class="loading">Loading profile...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <Sections v-else-if="profile">
      <Section standalone>
        <Placeholder
          :title="profile.name"
          caption="Your profile"
          standalone
        >
          <template #picture>
            <div class="profile-icon">👤</div>
          </template>
        </Placeholder>
      </Section>
      <Section padded>
        <div class="profile-details">
          <p><strong>Email:</strong> {{ profile.email }}</p>
          <p><strong>Bio:</strong> {{ profile.bio }}</p>
        </div>
      </Section>
    </Sections>
    <div v-else class="no-profile">No profile available.</div>
  </div>
</template>

<style scoped>
.profile-page {
  display: flex;
  flex-direction: column;
  min-height: 100%;
}

.profile-icon {
  font-size: 48px;
  width: var(--size-avatar-big);
  height: var(--size-avatar-big);
  display: flex;
  align-items: center;
  justify-content: center;
}

.profile-details {
  padding: var(--spacing-10);
  background-color: var(--color-bg-tertiary);
  border-radius: var(--size-border-radius-medium);
}

.profile-details p {
  margin: var(--spacing-5) 0;
}
</style>
