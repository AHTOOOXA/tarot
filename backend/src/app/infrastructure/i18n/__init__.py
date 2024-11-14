import json
from contextvars import ContextVar
from pathlib import Path
from typing import Callable, Dict, Optional

# Locales are now in backend/src/app/infrastructure/i18n/locales
LOCALES_DIR = Path(__file__).parent / "locales"

_translations: Dict[str, Dict[str, str]] = {}

current_i18n = ContextVar("current_i18n", default=None)


class I18nManager:
    def __init__(self):
        self._current_token: Optional[object] = None
        self._t: Optional[Callable] = None

    def set_translation(self, t: Callable):
        self._t = t
        self._current_token = current_i18n.set(self)

    def reset_translation(self):
        if self._current_token:
            current_i18n.reset(self._current_token)
            self._current_token = None
            self._t = None

    def __call__(self, key: str, *args, **kwargs) -> str:
        if self._t is None:
            raise RuntimeError("Translation function not set")
        return self._t(key, *args, **kwargs)


i18n = I18nManager()


def load_translations():
    for file in LOCALES_DIR.glob("*.json"):
        locale = file.stem
        with open(file, "r", encoding="utf-8") as f:
            _translations[locale] = json.load(f)


def get_translation(key: str, locale: str = "en") -> str:
    if not _translations:
        load_translations()
    return _translations.get(locale, {}).get(key, key)


def t(key: str, locale: Optional[str] = None) -> str:
    return get_translation(key, locale or "en")
