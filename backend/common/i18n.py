import glob
import json

from pathlib import Path
from typing import Any

import yaml

from backend.core.conf import settings
from backend.core.path_conf import LOCALE_DIR


class I18n:
    """Internationalization manager"""

    def __init__(self) -> None:
        self.locales: dict[str, dict[str, Any]] = {}
        self.current_language: str = settings.I18N_DEFAULT_LANGUAGE

    def load_locales(self) -> None:
        """Load language files"""
        patterns = [
            LOCALE_DIR / '*.json',
            LOCALE_DIR / '*.yaml',
            LOCALE_DIR / '*.yml',
        ]

        lang_files = []

        for pattern in patterns:
            lang_files.extend(glob.glob(str(pattern)))

        for lang_file in lang_files:
            with open(lang_file, encoding='utf-8') as f:
                lang = Path(lang_file).stem
                file_type = Path(lang_file).suffix[1:]
                match file_type:
                    case 'json':
                        self.locales[lang] = json.loads(f.read())
                    case 'yaml' | 'yml':
                        self.locales[lang] = yaml.full_load(f.read())

    def t(self, key: str, default: Any | None = None, **kwargs) -> str:
        """
        Translation function

        :param key: Target text key, supports dot notation, e.g. 'response.success'
        :param default: Default text when target language text does not exist
        :param kwargs: Variable parameters in target text
        :return:
        """
        keys = key.split('.')

        try:
            translation = self.locales[self.current_language]
        except KeyError:
            keys = 'error.language_not_found'
            translation = self.locales[settings.I18N_DEFAULT_LANGUAGE]

        for k in keys:
            if isinstance(translation, dict) and k in list(translation.keys()):
                translation = translation[k]
            else:
                # Pydantic compatibility
                translation = None if keys[0] == 'pydantic' else key

        if translation and kwargs:
            translation = translation.format(**kwargs)

        return translation or default


# Create i18n singleton
i18n = I18n()

# Create translation function instance
t = i18n.t
