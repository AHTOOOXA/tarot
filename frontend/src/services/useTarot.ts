import { useStatic } from './useStatic';

const { getStaticUrl } = useStatic();

const CARDS_PATH = 'images/moon_magic_tarot';

export function useTarot() {
  const getCardBackUrl = () => getStaticUrl(`${CARDS_PATH}/back.jpg`);

  const getCardUrl = (cardId: string) => getStaticUrl(`${CARDS_PATH}/${cardId}.jpg`);

  return {
    getCardBackUrl,
    getCardUrl,
  };
}
