import { defineStore } from 'pinia';

type ButtonClickHandler = () => void;

interface ButtonState {
  text: string;
  isVisible: boolean;
  isLoading: boolean;
  onClick: ButtonClickHandler | null;
}

export const useButtonStore = defineStore('button', {
  state: (): ButtonState => ({
    text: '',
    isVisible: false,
    isLoading: false,
    onClick: null,
  }),

  actions: {
    setButton(config: Partial<ButtonState>) {
      this.text = config.text ?? this.text;
      this.isVisible = config.isVisible ?? this.isVisible;
      this.onClick = config.onClick ?? this.onClick;
    },

    async handleClick() {
      if (!this.onClick) return;

      try {
        this.isLoading = true;
        await this.onClick();
      } catch (error) {
        console.error('Button click handler error:', error);
      } finally {
        this.isLoading = false;
      }
    },

    reset() {
      this.text = '';
      this.isVisible = false;
      this.isLoading = false;
      this.onClick = null;
    },
  },
});
