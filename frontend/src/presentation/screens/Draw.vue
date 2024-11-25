<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { Placeholder, Section, Sections, WithButton } from '@/presentation/components';
import { useTarot } from '@/services/useTarot';
import { useTelegram } from '@/services';

const { getCardBackUrl, getCardUrl } = useTarot();
const { closeApp } = useTelegram();

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
const showCardInfo = ref(false);
const showButton = ref(false);

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

  const flipPromises = otherCards.map((_, i) => flipCard(otherCards[i], i * 100));
  await Promise.all(flipPromises);
  await flipCard(selectedCard, otherCards.length * 100 - 50);
  showCardInfo.value = true;
  showButton.value = true;
};

onMounted(() => {
  setTimeout(() => {
    isVisible.value = true;
  }, 100);
});

const handleBackClick = () => {
  closeApp();
};
</script>

<template>
  <div
    class="draw-page"
    :class="{ hasDrawn }"
  >
    <Sections>
      <Section standalone>
        <Placeholder
          :title="showCardInfo && drawnCardIndex !== null ? cards[drawnCardIndex].name : 'Draw a Card'"
          :caption="showCardInfo ? 'The cards have spoken...' : 'Let the cards guide you'"
          standalone
          :class="{
            'fade-out': hasDrawn && !showCardInfo,
            'fade-in': showCardInfo,
          }"
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
  <WithButton
    v-if="showButton"
    button-text="Go back to bot"
    :button-click="handleBackClick"
  />
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
  gap: var(--spacing-32);
  padding: var(--spacing-8);
  perspective: 1000px;
  min-height: 360px;
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
  width: 85%;
  justify-content: space-evenly;
  max-width: 400px;
}

.card-wrapper {
  width: 90px;
  max-width: 140px;
  aspect-ratio: 550/966;
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
    selectedCardFlip 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) 0.8s forwards,
    selectedCardDance 8s ease-in-out 1.4s infinite;
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

  .cards-container {
    min-height: 400px;
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

@keyframes selectedCardDance {
  0% {
    transform: translateY(-40px) translateX(var(--initial-translate)) rotateY(180deg) rotate(var(--initial-rotate))
      scale(1.25);
  }
  10% {
    transform: translateY(-45px) translateX(calc(var(--initial-translate) + 8px)) rotateY(180deg)
      rotate(calc(var(--initial-rotate) + 3deg)) scale(1.35);
  }
  20% {
    transform: translateY(-35px) translateX(calc(var(--initial-translate) - 5px)) rotateY(180deg)
      rotate(calc(var(--initial-rotate) - 2deg)) scale(1.25);
  }
  30% {
    transform: translateY(-42px) translateX(calc(var(--initial-translate) - 3px)) rotateY(180deg)
      rotate(calc(var(--initial-rotate) + 1deg)) scale(1.32);
  }
  40% {
    transform: translateY(-38px) translateX(calc(var(--initial-translate) + 5px)) rotateY(540deg)
      rotate(calc(var(--initial-rotate) - 1deg)) scale(1.28);
  }
  50% {
    transform: translateY(-44px) translateX(calc(var(--initial-translate) + 3px)) rotateY(540deg)
      rotate(calc(var(--initial-rotate) + 2deg)) scale(1.33);
  }
  60% {
    transform: translateY(-36px) translateX(calc(var(--initial-translate) - 8px)) rotateY(540deg)
      rotate(calc(var(--initial-rotate) - 3deg)) scale(1.27);
  }
  70% {
    transform: translateY(-43px) translateX(calc(var(--initial-translate) + 6px)) rotateY(180deg)
      rotate(calc(var(--initial-rotate) + 2deg)) scale(1.34);
  }
  80% {
    transform: translateY(-37px) translateX(calc(var(--initial-translate) - 4px)) rotateY(180deg)
      rotate(calc(var(--initial-rotate) - 1deg)) scale(1.29);
  }
  90% {
    transform: translateY(-41px) translateX(calc(var(--initial-translate) + 7px)) rotateY(180deg)
      rotate(calc(var(--initial-rotate) + 3deg)) scale(1.31);
  }
  100% {
    transform: translateY(-40px) translateX(var(--initial-translate)) rotateY(180deg) rotate(var(--initial-rotate))
      scale(1.25);
  }
}

.fade-out {
  opacity: 0;
  transform: translateY(-20px);
  transition: all 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.fade-in {
  opacity: 1;
  transform: translateY(0);
  transition: all 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
}

/* Only apply initial hidden state when it's about to fade in */
.hasDrawn .placeholder:not(.fade-in):not(.fade-out) {
  transform: translateY(20px);
  opacity: 0;
}

.card-wrapper.flipped:not([data-selected='true']) {
  animation: cardEscape 0.8s cubic-bezier(0.34, 1.56, 0.64, 1) 2.3s forwards;
  /* Give each card a different escape direction using custom properties */
  &:nth-child(1) {
    --escape-x: -200%;
    --escape-y: -300%;
    --escape-rotate: -45deg;
  }
  &:nth-child(2) {
    --escape-x: 0%;
    --escape-y: -400%;
    --escape-rotate: 0deg;
  }
  &:nth-child(3) {
    --escape-x: 200%;
    --escape-y: -300%;
    --escape-rotate: 45deg;
  }
  &:nth-child(4) {
    --escape-x: -250%;
    --escape-y: -200%;
    --escape-rotate: -30deg;
  }
  &:nth-child(5) {
    --escape-x: 250%;
    --escape-y: -200%;
    --escape-rotate: 30deg;
  }
}

@keyframes cardEscape {
  to {
    opacity: 0;
    transform: translateX(var(--escape-x)) translateY(var(--escape-y)) rotateY(180deg)
      rotate(calc(var(--initial-rotate) + var(--escape-rotate))) scale(0.5);
  }
}
</style>
