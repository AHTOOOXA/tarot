import { createI18n } from 'vue-i18n';

const messages = {
  en: {
    draw: {
      loading: {
        title: 'Loading...',
        caption: 'Preparing your cards...',
      },
      placeholder: {
        title: 'Draw a Card',
        titleDrawn: '{cardName}',
        caption: 'Let the cards guide you',
        captionDrawn: 'The cards have spoken...',
      },
      button: 'Go back to bot',
      cardBack: 'Card back',
    },
  },
  ru: {
    draw: {
      loading: {
        title: 'Загрузка...',
        caption: 'Подготовка ваших карт...',
      },
      placeholder: {
        title: 'Вытянуть карту',
        titleDrawn: '{cardName}',
        caption: 'Позвольте картам направить вас',
        captionDrawn: 'Карты сказали своё слово...',
      },
      button: 'Вернуться к боту',
      cardBack: 'Рубашка карты',
    },
  },
};

export const i18n = createI18n({
  legacy: false, // Use Composition API
  locale: 'en',
  fallbackLocale: 'en',
  messages,
});
