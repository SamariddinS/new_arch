from pathlib import Path

# Project root directory
BASE_PATH = Path(__file__).resolve().parent.parent

# Alembic migration files storage path
ALEMBIC_VERSION_DIR = BASE_PATH / 'alembic' / 'versions'

# Log file path
LOG_DIR = BASE_PATH / 'log'

# Static resources directory
STATIC_DIR = BASE_PATH / 'static'

# Upload file directory
UPLOAD_DIR = STATIC_DIR / 'upload'

# Plugin directory
PLUGIN_DIR = BASE_PATH / 'plugin'

# Internationalization file directory
LOCALE_DIR = BASE_PATH / 'locale'
