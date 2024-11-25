<script setup lang="ts">
import { ref } from 'vue';
import { Placeholder, Section, Sections, List, ListItem } from '@/presentation/components';

const cards = ref([
  {
    name: 'The Fool',
    isDrawn: false,
    position: 0,
  },
  {
    name: 'The Magician',
    isDrawn: false,
    position: 1,
  },
  {
    name: 'The High Priestess',
    isDrawn: false,
    position: 2,
  },
]);

const isDrawing = ref(false);
const drawnCard = ref<string | null>(null);

const drawCard = () => {
  isDrawing.value = true;

  // Simulate card drawing animation
  setTimeout(() => {
    const undrawnCards = cards.value.filter(card => !card.isDrawn);
    if (undrawnCards.length) {
      const randomIndex = Math.floor(Math.random() * undrawnCards.length);
      const card = undrawnCards[randomIndex];
      card.isDrawn = true;
      drawnCard.value = card.name;
    }
    isDrawing.value = false;
  }, 1000);
};
</script>

<template>
  <div class="draw-page">
    <Sections>
      <Section standalone>
        <Placeholder
          title="Draw a Card"
          caption="Let the cards guide you"
          standalone
        >
          <template #picture>
            <div class="draw-icon">🎴</div>
          </template>
        </Placeholder>
      </Section>
      <Section padded>
        <div class="draw-content">
          <div
            class="draw-area"
            :class="{ drawing: isDrawing }"
            @click="drawCard"
          >
            <span v-if="drawnCard">{{ drawnCard }}</span>
            <span v-else>Tap to draw a card</span>
          </div>

          <List
            standalone
            gapped
          >
            <ListItem
              v-for="card in cards"
              :key="card.position"
              :title="card.name"
              :subtitle="card.isDrawn ? 'Drawn' : 'Not drawn'"
              icon="🎴"
              :is-emoji="true"
              :class="{ drawn: card.isDrawn }"
            />
          </List>
        </div>
      </Section>
    </Sections>
  </div>
</template>

<style scoped>
.draw-page {
  display: flex;
  flex-direction: column;
  min-height: 100%;
}

.draw-icon {
  font-size: 48px;
  width: var(--size-avatar-big);
  height: var(--size-avatar-big);
  display: flex;
  align-items: center;
  justify-content: center;
}

.draw-content {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-10);
}

.draw-area {
  padding: var(--spacing-16);
  background-color: var(--color-bg-tertiary);
  border-radius: var(--size-border-radius-medium);
  text-align: center;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.draw-area.drawing {
  transform: scale(0.95);
}

.drawn {
  opacity: 0.5;
}
</style>
