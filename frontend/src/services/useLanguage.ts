import { i18n } from '@/i18n';
import { useUserStore } from '@/store/user';
import { watch } from 'vue';
import { storeToRefs } from 'pinia';

// Default fallback locale
const DEFAULT_LOCALE = 'en';
const SUPPORTED_LOCALES = ['en', 'ru'] as const;

type SupportedLocale = (typeof SUPPORTED_LOCALES)[number];

export function useLanguage() {
  const userStore = useUserStore();
  const { user } = storeToRefs(userStore);

  const getUserLocale = (appLangCode = '', langCode = ''): SupportedLocale => {
    const lang = (appLangCode || langCode).toLowerCase();
    return SUPPORTED_LOCALES.includes(lang as SupportedLocale) ? (lang as SupportedLocale) : DEFAULT_LOCALE;
  };

  watch(
    () => user.value,
    newUser => {
      if (newUser) {
        const locale = getUserLocale(newUser.app_language_code ?? '', newUser.language_code ?? '');
        i18n.global.locale.value = locale;
      }
    },
    { immediate: true }
  );

  const setLanguage = (lang: string) => {
    const locale = getUserLocale(lang);
    i18n.global.locale.value = locale;
  };

  return {
    setLanguage,
    getUserLocale,
  };
}
