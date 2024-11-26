<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { Placeholder, Section, Sections, WithButton } from '@/presentation/components';
import { useTelegram } from '@/services';
import { storeToRefs } from 'pinia';
import { useTarotStore } from '@/store/tarot';
import { useStatic } from '@/services';

const { closeApp } = useTelegram();
const { getStaticUrl, preloadImage } = useStatic();

const tarotStore = useTarotStore();
const { cards } = storeToRefs(tarotStore);

const drawnCardIndex = ref<number | null>(null);
const isVisible = ref(false);
const hasDrawn = ref(false);
const showCardInfo = ref(false);
const showButton = ref(false);
const isLoading = ref(true);
const imageUrls = ref<Record<string, string>>({});
const cardBackUrl = 'images/moon_magic_tarot/back.jpg';

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

  setTimeout(() => {
    otherCards.forEach(card => card.classList.add('escaping'));
  }, 150);

  showCardInfo.value = true;
  showButton.value = true;
};

onMounted(async () => {
  try {
    // Preload all images
    const [cardsData] = await Promise.all([
      tarotStore.fetchDailyCards(),
      preloadImage(cardBackUrl),
      // Preload all card images
      ...cards.value.map(card => preloadImage(card.image_url)),
    ]);

    // Cache URLs
    imageUrls.value = {
      back: getStaticUrl(cardBackUrl),
      ...Object.fromEntries(cards.value.map(card => [card.key, getStaticUrl(card.image_url)])),
    };

    isVisible.value = true;
    isLoading.value = false;
  } catch (error) {
    console.error('Failed to initialize:', error);
  }
});

const handleBackClick = () => {
  closeApp();
};
</script>

<template>
  <div
    v-if="!isLoading"
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
                    :src="imageUrls.back"
                    alt="Card back"
                  />
                </div>
                <div class="card-front">
                  <img
                    :src="imageUrls[card.key]"
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
                    :src="imageUrls.back"
                    alt="Card back"
                  />
                </div>
                <div class="card-front">
                  <img
                    :src="imageUrls[card.key]"
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
  <div
    v-else
    class="loading-container"
  >
    <Placeholder
      title="Loading..."
      caption="Preparing your cards..."
      standalone
    />
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

.top-row .card-wrapper:first-child {
  --extra-translate: 90px;
}

.top-row .card-wrapper:last-child {
  --extra-translate: -90px;
}

.middle-row .card-wrapper:first-child {
  --extra-translate: 50px;
}

.middle-row .card-wrapper:last-child {
  --extra-translate: -50px;
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
  --card-direction: 1; /* Default direction for top row */
  --extra-translate: 0px; /* Default no extra translation */
}

.middle-row .card-wrapper {
  --card-direction: -1;
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
    scale(1.4);
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
    transform: translateY(0) translateX(calc(var(--initial-translate) + 0 * var(--extra-translate))) rotateY(0)
      rotate(var(--initial-rotate)) scale(1);
  }
  15% {
    transform: translateY(calc(var(--card-direction) * 45px))
      translateX(calc(var(--initial-translate) + 0.15 * var(--extra-translate) - 35px))
      rotate(calc(var(--initial-rotate) - 5deg)) scale(1.15);
  }
  30% {
    transform: translateY(calc(var(--card-direction) * 60px))
      translateX(calc(var(--initial-translate) + 0.3 * var(--extra-translate) + 35px))
      rotate(calc(var(--initial-rotate) + 5deg)) scale(1.25);
  }
  45% {
    transform: translateY(calc(var(--card-direction) * 55px))
      translateX(calc(var(--initial-translate) + 0.45 * var(--extra-translate) - 30px))
      rotate(calc(var(--initial-rotate) - 4deg)) scale(1.25);
  }
  60% {
    transform: translateY(calc(var(--card-direction) * 60px))
      translateX(calc(var(--initial-translate) + 0.6 * var(--extra-translate) + 30px))
      rotate(calc(var(--initial-rotate) + 4deg)) scale(1.25);
  }
  75% {
    transform: translateY(calc(var(--card-direction) * 55px))
      translateX(calc(var(--initial-translate) + 0.75 * var(--extra-translate) - 25px))
      rotate(calc(var(--initial-rotate) - 3deg)) scale(1.25);
  }
  90%,
  100% {
    transform: translateY(calc(var(--card-direction) * 60px))
      translateX(calc(var(--initial-translate) + 1 * var(--extra-translate))) rotate(var(--initial-rotate)) scale(1.4);
  }
}

@keyframes selectedCardFlip {
  0% {
    transform: translateY(calc(var(--card-direction) * 60px))
      translateX(calc(var(--initial-translate) + var(--extra-translate))) rotate(var(--initial-rotate)) scale(1.4);
  }
  100% {
    transform: translateY(calc(var(--card-direction) * 60px))
      translateX(calc(var(--initial-translate) + var(--extra-translate))) rotateY(180deg) rotate(var(--initial-rotate))
      scale(1.4);
  }
}

@keyframes selectedCardDance {
  0% {
    transform: translateY(calc(var(--card-direction) * 60px))
      translateX(calc(var(--initial-translate) + var(--extra-translate))) rotateY(180deg) rotate(var(--initial-rotate))
      scale(1.4);
  }
  10% {
    transform: translateY(calc(var(--card-direction) * 70px))
      translateX(calc(var(--initial-translate) + var(--extra-translate) + 12px)) rotateY(180deg)
      rotate(calc(var(--initial-rotate) + 3deg)) scale(1.5);
  }
  20% {
    transform: translateY(calc(var(--card-direction) * 55px))
      translateX(calc(var(--initial-translate) + var(--extra-translate) - 8px)) rotateY(180deg)
      rotate(calc(var(--initial-rotate) - 2deg)) scale(1.4);
  }
  30% {
    transform: translateY(calc(var(--card-direction) * 65px))
      translateX(calc(var(--initial-translate) + var(--extra-translate) - 5px)) rotateY(180deg)
      rotate(calc(var(--initial-rotate) + 1deg)) scale(1.47);
  }
  40% {
    transform: translateY(calc(var(--card-direction) * 58px))
      translateX(calc(var(--initial-translate) + var(--extra-translate) + 8px)) rotateY(540deg)
      rotate(calc(var(--initial-rotate) - 1deg)) scale(1.43);
  }
  50% {
    transform: translateY(calc(var(--card-direction) * 68px))
      translateX(calc(var(--initial-translate) + var(--extra-translate) + 5px)) rotateY(540deg)
      rotate(calc(var(--initial-rotate) + 2deg)) scale(1.48);
  }
  60% {
    transform: translateY(calc(var(--card-direction) * 56px))
      translateX(calc(var(--initial-translate) + var(--extra-translate) - 12px)) rotateY(540deg)
      rotate(calc(var(--initial-rotate) - 3deg)) scale(1.42);
  }
  70% {
    transform: translateY(calc(var(--card-direction) * 66px))
      translateX(calc(var(--initial-translate) + var(--extra-translate) + 9px)) rotateY(180deg)
      rotate(calc(var(--initial-rotate) + 2deg)) scale(1.49);
  }
  80% {
    transform: translateY(calc(var(--card-direction) * 57px))
      translateX(calc(var(--initial-translate) + var(--extra-translate) - 6px)) rotateY(180deg)
      rotate(calc(var(--initial-rotate) - 1deg)) scale(1.44);
  }
  90% {
    transform: translateY(calc(var(--card-direction) * 64px))
      translateX(calc(var(--initial-translate) + var(--extra-translate) + 10px)) rotateY(180deg)
      rotate(calc(var(--initial-rotate) + 3deg)) scale(1.46);
  }
  100% {
    transform: translateY(calc(var(--card-direction) * 60px))
      translateX(calc(var(--initial-translate) + var(--extra-translate))) rotateY(180deg) rotate(var(--initial-rotate))
      scale(1.4);
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

.card-wrapper.escaping {
  animation: cardEscape 0.8s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
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

.loading-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
}
</style>
