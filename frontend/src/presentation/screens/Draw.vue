<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { Placeholder, Section, Sections } from '@/presentation/components';
import { useTarot } from '@/services/useTarot';

const { getCardBackUrl } = useTarot();

const isDrawing = ref(false);
const drawnCard = ref<string | null>(null);
const isVisible = ref(false);

const drawCard = () => {
  isDrawing.value = true;
  // Simulate card drawing animation
  setTimeout(() => {
    isDrawing.value = false;
  }, 1000);
};

onMounted(() => {
  // Trigger the appearance animation after mount
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
        >
          <!-- <template #picture>
            <div class="draw-icon">🎴</div>
          </template> -->
        </Placeholder>
      </Section>
      <Section padded>
        <div class="draw-content">
          <div class="cards-container">
            <div class="cards-row top-row">
              <div
                v-for="i in 3"
                :key="i"
                class="card-back"
                :class="{
                  drawing: isDrawing,
                  visible: isVisible,
                }"
                :style="{
                  '--appear-delay': `${(i - 1) * 150}ms`,
                  '--initial-rotate': `${(i - 2) * 10}deg`,
                  '--initial-translate': `${(i - 2) * 20}px`,
                }"
                @click="drawCard"
              >
                <img
                  :src="getCardBackUrl()"
                  alt="Card back"
                />
              </div>
            </div>
            <div class="cards-row middle-row">
              <div
                v-for="i in 2"
                :key="i + 3"
                class="card-back"
                :class="{
                  drawing: isDrawing,
                  visible: isVisible,
                }"
                :style="{
                  '--appear-delay': `${(i + 2) * 150}ms`,
                  '--initial-rotate': `${(i - 1.5) * 10}deg`,
                  '--initial-translate': `${(i - 1.5) * 20}px`,
                }"
                @click="drawCard"
              >
                <img
                  :src="getCardBackUrl()"
                  alt="Card back"
                />
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

.card-back {
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

.card-back.visible {
  opacity: 1;
  transform: translateY(0) translateX(var(--initial-translate)) rotateY(0) rotate(var(--initial-rotate)) rotateZ(0deg);
  transition-delay: var(--appear-delay);
}

.card-back img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: var(--size-border-radius-small);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  backface-visibility: hidden;
}

.card-back.drawing {
  transform: scale(0.95) translateX(var(--initial-translate)) rotate(var(--initial-rotate));
}

.card-back:hover {
  transform: translateY(-10px) translateX(var(--initial-translate)) rotate(var(--initial-rotate)) scale(1.05);
  z-index: 1;
}

@media (min-width: 768px) {
  .card-back {
    width: 120px;
  }
}
</style>
