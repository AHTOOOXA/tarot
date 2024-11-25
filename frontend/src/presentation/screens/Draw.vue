<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { Placeholder, Section, Sections } from '@/presentation/components';
import { useTarot } from '@/services/useTarot';

const { getCardBackUrl, getCardUrl } = useTarot();

interface Card {
  key: string;
  name: string;
}

const cards = ref<Card[]>([
  { key: '0', name: 'The Fool' },
  { key: '1', name: 'The Magician' },
  { key: '2', name: 'The High Priestess' },
  { key: '3', name: 'The Empress' },
  { key: '4', name: 'The Emperor' },
]);

const drawnCardIndex = ref<number | null>(null);
const isVisible = ref(false);
const hasDrawn = ref(false);

const flipCard = (element: Element, delay: number = 0) => {
  return new Promise<void>(resolve => {
    setTimeout(() => {
      element.classList.add('flipped');
      // Wait for flip animation to complete
      setTimeout(resolve, 800);
    }, delay);
  });
};

const drawCard = async (index: number) => {
  if (hasDrawn.value) return;

  drawnCardIndex.value = index;
  hasDrawn.value = true;

  const cardElements = document.querySelectorAll('.card-wrapper');
  const otherCards = Array.from(cardElements).filter((_, i) => i !== index);
  const selectedCard = cardElements[index];

  // Always flip cards in the same order: top row left to right, then bottom row left to right
  const flipPromises = otherCards.map((_, i) => flipCard(otherCards[i], i * 100));

  // Wait for all other cards to flip
  await Promise.all(flipPromises);

  // Flip the selected card last with consistent timing
  await flipCard(selectedCard, otherCards.length * 100 - 50);
};

onMounted(() => {
  setTimeout(() => {
    isVisible.value = true;
  }, 100);
});
</script>

<template>
  <div class="draw-page">
    <Sections>
      <Section standalone>
        <Placeholder
          title="Draw a Card"
          caption="Let the cards guide you"
          standalone
        />
      </Section>
      <Section padded>
        <div class="draw-content">
          <div class="cards-container">
            <div class="cards-row top-row">
              <div
                v-for="(card, i) in cards.slice(0, 3)"
                :key="card.key"
                class="card-wrapper"
                :class="{
                  visible: isVisible,
                  'can-draw': !hasDrawn,
                }"
                :data-selected="drawnCardIndex === i"
                :style="{
                  '--appear-delay': `${i * 150}ms`,
                  '--initial-rotate': `${(i - 1) * 10}deg`,
                  '--initial-translate': `${(i - 1) * 20}px`,
                }"
                @click="!hasDrawn && drawCard(i)"
              >
                <div class="card-back">
                  <img
                    :src="getCardBackUrl()"
                    alt="Card back"
                  />
                </div>
                <div class="card-front">
                  <img
                    :src="getCardUrl(card.key)"
                    :alt="card.name"
                  />
                </div>
              </div>
            </div>
            <div class="cards-row middle-row">
              <div
                v-for="(card, i) in cards.slice(3, 5)"
                :key="card.key"
                class="card-wrapper"
                :class="{
                  visible: isVisible,
                  'can-draw': !hasDrawn,
                }"
                :data-selected="drawnCardIndex === i + 3"
                :style="{
                  '--appear-delay': `${(i + 3) * 150}ms`,
                  '--initial-rotate': `${(i - 0.5) * 10}deg`,
                  '--initial-translate': `${(i - 0.5) * 20}px`,
                }"
                @click="!hasDrawn && drawCard(i + 3)"
              >
                <div class="card-back">
                  <img
                    :src="getCardBackUrl()"
                    alt="Card back"
                  />
                </div>
                <div class="card-front">
                  <img
                    :src="getCardUrl(card.key)"
                    :alt="card.name"
                  />
                </div>
              </div>
            </div>
          </div>
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

.cards-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-24);
  padding: var(--spacing-16);
  perspective: 1000px;
  min-height: 300px;
}

.cards-row {
  display: flex;
  justify-content: center;
  margin: var(--spacing-8);
}

.top-row {
  width: 100%;
  justify-content: space-evenly;
  max-width: 500px;
}

.middle-row {
  width: 80%;
  justify-content: space-evenly;
  max-width: 400px;
}

.card-wrapper {
  width: 90px;
  max-width: 140px;
  aspect-ratio: 1/1.4;
  cursor: pointer;
  opacity: 0;
  transform: translateY(100px) translateX(var(--initial-translate)) rotateY(180deg) rotate(var(--initial-rotate))
    rotateZ(45deg);
  transition: all 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);
  position: relative;
  transform-style: preserve-3d;
}

.card-wrapper.visible {
  opacity: 1;
  transform: translateY(0) translateX(var(--initial-translate)) rotateY(0) rotate(var(--initial-rotate)) rotateZ(0deg);
  transition-delay: var(--appear-delay);
}

.card-wrapper.flipped {
  transform: translateY(0) translateX(var(--initial-translate)) rotateY(180deg) rotate(var(--initial-rotate));
}

.card-wrapper.flipped[data-selected='true'] {
  opacity: 1;
  z-index: 10;
  transform: translateY(-40px) translateX(var(--initial-translate)) rotateY(180deg) rotate(var(--initial-rotate))
    scale(1.25);
  animation:
    selectedCardShake 0.8s cubic-bezier(0.36, 0, 0.66, -0.56),
    selectedCardFlip 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) 0.8s forwards;
}

.card-wrapper.can-draw:hover {
  transform: translateY(-10px) translateX(var(--initial-translate)) rotate(var(--initial-rotate)) scale(1.05);
  z-index: 1;
}

.card-wrapper:not(.can-draw) {
  cursor: default;
}

.card-back,
.card-front {
  position: absolute;
  width: 100%;
  height: 100%;
  backface-visibility: hidden;
  transform-style: preserve-3d;
}

.card-front {
  transform: rotateY(180deg);
}

.card-back img,
.card-front img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: var(--size-border-radius-small);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

@media (min-width: 768px) {
  .card-wrapper {
    width: 120px;
  }
}

@keyframes selectedCardShake {
  0% {
    transform: translateY(0) translateX(var(--initial-translate)) rotateY(0) rotate(var(--initial-rotate)) scale(1);
  }
  15% {
    transform: translateY(-30px) translateX(calc(var(--initial-translate) - 25px))
      rotate(calc(var(--initial-rotate) - 5deg)) scale(1.15);
  }
  30% {
    transform: translateY(-40px) translateX(calc(var(--initial-translate) + 25px))
      rotate(calc(var(--initial-rotate) + 5deg)) scale(1.25);
  }
  45% {
    transform: translateY(-35px) translateX(calc(var(--initial-translate) - 20px))
      rotate(calc(var(--initial-rotate) - 4deg)) scale(1.25);
  }
  60% {
    transform: translateY(-40px) translateX(calc(var(--initial-translate) + 20px))
      rotate(calc(var(--initial-rotate) + 4deg)) scale(1.25);
  }
  75% {
    transform: translateY(-35px) translateX(calc(var(--initial-translate) - 15px))
      rotate(calc(var(--initial-rotate) - 3deg)) scale(1.25);
  }
  90%,
  100% {
    transform: translateY(-40px) translateX(var(--initial-translate)) rotate(var(--initial-rotate)) scale(1.25);
  }
}

@keyframes selectedCardFlip {
  0% {
    transform: translateY(-40px) translateX(var(--initial-translate)) rotate(var(--initial-rotate)) scale(1.25);
  }
  100% {
    transform: translateY(-40px) translateX(var(--initial-translate)) rotateY(180deg) rotate(var(--initial-rotate))
      scale(1.25);
  }
}
</style>
