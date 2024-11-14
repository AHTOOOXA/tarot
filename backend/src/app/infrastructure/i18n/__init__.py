import json
from pathlib import Path
from typing import Dict, Optional

# Locales are now in backend/src/app/infrastructure/i18n/locales
LOCALES_DIR = Path(__file__).parent / "locales"

_translations: Dict[str, Dict[str, str]] = {}


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
