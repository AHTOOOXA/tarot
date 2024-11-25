<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { Placeholder, Section, Sections } from '@/presentation/components';
import { useUserStore } from '@/store/user';

const userStore = useUserStore();
const isLoading = ref(true);
const error = ref<string | null>(null);

const user = computed(() => userStore.getUser);

onMounted(async () => {
  try {
    isLoading.value = true;
    await userStore.fetchUser();
    console.log('Loaded profile:', user.value);
  } catch (e) {
    error.value = 'Failed to load profile. Please try again later.';
    console.error('Error loading profile:', e);
  } finally {
    isLoading.value = false;
  }
});
</script>

<template>
  <div class="profile-page">
    <div
      v-if="isLoading"
      class="loading"
    >
      Loading profile...
    </div>
    <div
      v-else-if="error"
      class="error"
    >
      {{ error }}
    </div>
    <Sections v-else-if="user">
      <Section standalone>
        <Placeholder
          :title="user.first_name + (user.last_name ? ' ' + user.last_name : '')"
          :caption="user.username ? '@' + user.username : 'Your profile'"
          standalone
        >
          <template #picture>
            <img
              v-if="user.photo_url"
              :src="user.photo_url"
              alt="Profile Picture"
              class="profile-picture"
            />
            <div
              v-else
              class="profile-icon"
            >
              👤
            </div>
          </template>
        </Placeholder>
      </Section>
      <Section padded>
        <div class="profile-details">
          <p><strong>User ID:</strong> {{ user.user_id }}</p>
          <p v-if="user.username"><strong>Username:</strong> @{{ user.username }}</p>
          <p><strong>First Name:</strong> {{ user.first_name }}</p>
          <p v-if="user.last_name"><strong>Last Name:</strong> {{ user.last_name }}</p>
          <p v-if="user.language_code"><strong>Language:</strong> {{ user.language_code }}</p>
        </div>
      </Section>
    </Sections>
    <div
      v-else
      class="no-profile"
    >
      No profile available.
    </div>
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

.profile-picture {
  width: var(--size-avatar-big);
  height: var(--size-avatar-big);
  border-radius: 50%;
  object-fit: cover;
}
</style>
